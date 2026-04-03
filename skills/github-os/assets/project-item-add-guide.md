# Project Item-Add Guide

## The Problem

When adding an issue to a GitHub Project via the GraphQL API, the `addProjectV2ItemById` mutation requires a **content ID** (the issue's global node ID), not a database ID or local item ID.

Adding issues via the GitHub web UI or `gh issue add` works fine, but programmatic approaches often hit this snag because there are three different ID types in play, and the mutation is picky about which one it accepts.

## The Three ID Types

| ID Type               | Example                        | Scope                 | Used As                                     |
| --------------------- | ------------------------------ | --------------------- | ------------------------------------------- |
| Issue number          | `30`                           | Repository            | Human reference, URL slug, CLI flags        |
| Issue node ID         | `I_kwDORWG4i876VLo4`           | Global (GitHub graph) | `contentId` in `addProjectV2ItemById`       |
| Local project item ID | `PVTI_lAHOAKCne84BSNIEzgpDMT8` | Project V2 only       | `itemId` in `updateProjectV2ItemFieldValue` |

The critical confusion: the local item ID (returned by a successful `addProjectV2ItemById`) looks like a node ID but only works within that specific project. It cannot be used as `contentId` on any mutation.

## The Workflow

### Step 1 — Get the issue's node ID

```bash
gh api repos/{owner}/{repo}/issues/{number} --jq '{number, node_id, title}'
```

Example output:

```json
{
  "number": 42,
  "node_id": "I_kwDORWG4i876VLo4",
  "title": "Add dark mode support"
}
```

Extract the `node_id` field — that is your `contentId`.

### Step 2 — Add the issue to the project

```bash
gh api graphql -f query='mutation {
  addProjectV2ItemById(input: {
    projectId: "<PROJECT_ID>"
    contentId: "<ISSUE_NODE_ID>"
  }) {
    item { id }
  }
}'
```

Replace:

- `<PROJECT_ID>` — the project node ID (e.g. `<PROJECT_ID>`)
- `<ISSUE_NODE_ID>` — the `node_id` from Step 1 (e.g. `I_kwDORWG4i876VLo4`)

Returns the new **local project item ID** (e.g. `PVTI_lAHOAKCne84BSNIEzgpDMT8`). Save this — it is needed for field updates.

### Step 3 — Set project fields (optional)

Use the **local project item ID** from Step 2, not the issue node ID:

```bash
gh api graphql -f query='mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "<PROJECT_ID>"
    itemId: "<LOCAL_PROJECT_ITEM_ID>"
    fieldId: "<FIELD_ID>"
    value: { singleSelectOptionId: "<OPTION_ID>" }
  }) {
    projectV2Item { id }
  }
}'
```

Where:

- `<LOCAL_PROJECT_ITEM_ID>` — returned by Step 2 (e.g. `PVTI_lAHOAKCne84BSNIEzgpDMT8`)
- `<FIELD_ID>` — the field's node ID (e.g. `PVTSSF_lAHOAKCne84BSNIEzg_ztnE` for Status)
- `<OPTION_ID>` — the option's ID (e.g. `f75ad846` for "Todo")

To discover field IDs and option IDs:

```bash
gh api graphql -f query='query { node(id: "<PROJECT_ID>") {
  ... on ProjectV2 {
    fields(first: 20) {
      nodes {
        ... on ProjectV2SingleSelectField { id name options { id name } }
        ... on ProjectV2Field { id name }
      }
    }
  }
}}'
```

## Common Mistakes

### Mistake 1 — Using the issue number

```bash
# WRONG
gh api graphql -f query='mutation { addProjectV2ItemById(input: {
  projectId: "PVT_xxxx"
  contentId: "42"   # ← issue number is not a valid contentId
}) { item { id } } }'
```

Error: `Could not resolve to a node with the global id of '42'`

### Mistake 2 — Using the local project item ID as contentId

```bash
# WRONG
gh api graphql -f query='mutation { addProjectV2ItemById(input: {
  projectId: "PVT_xxxx"
  contentId: "PVTI_lAHOAKCne84BSNIEzgpDMT8"   # ← this is a local item ID, not a global node ID
}) { item { id } } }'
```

Error: `Could not resolve to a node with the global id of 'PVTI_lAHOAKCne84BSNIEzgpDMT8'`

### Mistake 3 — Using itemId instead of contentId

```bash
# WRONG — wrong parameter name
gh api graphql -f query='mutation { addProjectV2ItemById(input: {
  projectId: "PVT_xxxx"
  itemId: "I_kwDORWG4i876VLo4"   # ← itemId is not a valid argument
}) { item { id } } }'
```

Error: `InputObject 'AddProjectV2ItemByIdInput' doesn't accept argument 'itemId'`

## Script Template

```bash
#!/usr/bin/env bash
# add-to-project.sh — adds an issue to a GitHub Project and optionally sets fields

# --- Configuration ---
OWNER="<owner>"           # e.g. myorg
REPO="<repo>"             # e.g. my-repo
PROJECT_ID="<PROJECT_ID>" # e.g. <PROJECT_ID>
ISSUE_NUM="<number>"     # e.g. 42
FIELD_ID="<FIELD_ID>"    # e.g. PVTSSF_xxx for Status
OPTION_ID="<OPTION_ID>"  # e.g. f75ad846 for Todo

# --- Step 1: Get issue node ID ---
ISSUE_NODE_ID=$(gh api repos/${OWNER}/${REPO}/issues/${ISSUE_NUM} --jq '.node_id')
echo "Issue node ID: ${ISSUE_NODE_ID}"

# --- Step 2: Add to project ---
LOCAL_ITEM_ID=$(gh api graphql --jq '.data.addProjectV2ItemById.item.id' -f query="mutation { addProjectV2ItemById(input: { projectId: \"${PROJECT_ID}\", contentId: \"${ISSUE_NODE_ID}\" }) { item { id } } }")
echo "Local project item ID: ${LOCAL_ITEM_ID}"

# --- Step 3: Set status to Todo ---
gh api graphql -f query="mutation { updateProjectV2ItemFieldValue(input: { projectId: \"${PROJECT_ID}\", itemId: \"${LOCAL_ITEM_ID}\", fieldId: \"${FIELD_ID}\", value: { singleSelectOptionId: \"${OPTION_ID}\" } }) { projectV2Item { id } } }"
echo "Done."
```

## References

- [GitHub GraphQL API — ProjectsV2](https://docs.github.com/en/graphql/reference/mutations#addprojectv2itembyid)
- [GitHub CLI — gh api](https://cli.github.com/manual/gh_api)
