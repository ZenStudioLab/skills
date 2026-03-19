# GitHub MCP Server Setup Guide

The GitHub Model Context Protocol (MCP) server enables AI agents to interact with GitHub directly. This is the **primary tool** for the GitHub OS skill.

## Installation

### Option 1: Global Installation (Recommended)

```bash
npm install -g @modelcontextprotocol/server-github
```

### Option 2: Project-Specific

```bash
npm install --save-dev @modelcontextprotocol/server-github
```

## Configuration

### For Windsurf IDE

Add to your IDE's MCP configuration file (usually `~/.windsurf/mcp-config.json`):

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

### For Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

### For Other IDEs

Check your IDE's MCP documentation for configuration location.

## GitHub Token Setup

### 1. Create Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" > "Generate new token (classic)"
3. Name: "MCP Server"
4. Select scopes:
   - ✅ `repo` (full control of private repositories)
   - ✅ `read:org` (read organization data)
   - ✅ `project` (full control of projects)
5. Click "Generate token"
6. **Copy the token** (you won't see it again)

### 2. Set Token in Configuration

Replace `your_github_token_here` in the config file with your actual token.

**Security Note**: Never commit tokens to git. Use environment variables in production.

### 3. Alternative: Environment Variable

Instead of hardcoding in config:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

Then set in your shell:

```bash
export GITHUB_TOKEN="your_token_here"
```

## Verification

### Test Connection

Ask your AI agent:

```
Can you list my GitHub repositories?
```

If MCP is working, the agent will use the GitHub MCP server to fetch your repos.

### Check Available Tools

Ask your AI agent:

```
What GitHub MCP tools are available?
```

You should see tools like:
- `mcp3_create_or_update_file`
- `mcp3_issue_write`
- `mcp3_create_pull_request`
- `mcp3_list_issues`
- etc.

## Troubleshooting

### Error: "GitHub MCP server not found"

**Cause**: Server not installed or not in PATH

**Solution**:
```bash
npm install -g @modelcontextprotocol/server-github
```

### Error: "Authentication failed"

**Cause**: Invalid or missing GitHub token

**Solution**:
1. Check token in config file
2. Verify token hasn't expired
3. Verify token has correct scopes
4. Generate new token if needed

### Error: "Permission denied"

**Cause**: Token lacks required scopes

**Solution**:
1. Go to token settings: https://github.com/settings/tokens
2. Edit token
3. Add missing scopes (`repo`, `project`)
4. Update token in config

### Error: "Rate limit exceeded"

**Cause**: Too many API requests

**Solution**:
1. Wait for rate limit to reset
2. Use authenticated token (higher limits)
3. Reduce request frequency

## Fallback: GitHub CLI

If GitHub MCP is unavailable, use GitHub CLI (`gh`) as fallback:

### Install GitHub CLI

**macOS**:
```bash
brew install gh
```

**Linux**:
```bash
# Debian/Ubuntu
sudo apt install gh

# Fedora/RHEL
sudo dnf install gh
```

**Windows**:
```bash
winget install GitHub.cli
```

### Authenticate

```bash
gh auth login
```

Follow prompts to authenticate.

### Verify

```bash
gh repo list
```

## Usage Examples

### Create Label (via MCP)

```javascript
mcp3_create_label({
  owner: "username",
  repo: "repo-name",
  name: "type:feature",
  color: "0e8a16",
  description: "New features"
})
```

### Create Issue (via MCP)

```javascript
mcp3_issue_write({
  method: "create",
  owner: "username",
  repo: "repo-name",
  title: "Implement SSO",
  body: "Full issue body here",
  labels: ["type:feature", "priority:p1"]
})
```

### Create File (via MCP)

```javascript
mcp3_create_or_update_file({
  owner: "username",
  repo: "repo-name",
  path: ".github/ISSUE_TEMPLATE/task.yml",
  content: "template content here",
  message: "Add task template",
  branch: "main"
})
```

## Resources

- GitHub MCP Server: https://github.com/modelcontextprotocol/servers/tree/main/src/github
- MCP Documentation: https://modelcontextprotocol.io
- GitHub API: https://docs.github.com/en/rest
- GitHub CLI: https://cli.github.com

## Support

If you encounter issues:

1. Check GitHub MCP server logs
2. Verify GitHub token validity
3. Test with GitHub CLI as fallback
4. Open issue: https://github.com/modelcontextprotocol/servers/issues
