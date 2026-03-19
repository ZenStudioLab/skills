# Repository Analysis Example: Single Repo

## Input

**Repository**: `company/myapp`

**Structure**:
```
myapp/
├── src/
│   ├── components/
│   ├── services/
│   └── utils/
├── tests/
├── docs/
│   ├── architecture.md
│   ├── ADRs/
│   │   ├── 0001-tech-stack.md
│   │   └── 0002-state-management.md
│   └── api/
├── package.json
└── README.md
```

## Analysis Output

### Repository Type
**Single Repository**

### Modules Detected
- **main** (type: app, path: ./src)

### Documentation Structure
- **Docs directory**: `./docs`
- **Architecture docs**: ✅ Found (`./docs/architecture.md`)
- **ADRs**: ✅ Found (`./docs/ADRs/` with 2 records)
- **Assessment**: Rich

### Execution Surfaces
- **Primary repo**: company/myapp
- **Total modules**: 1
- **Recommended label count**: 10
  - 4 type labels
  - 4 priority labels
  - 2 area labels (minimal for single app)

## GitHub OS Design

### Labels (10 total)

**Type** (4):
- `type:feature` - New features
- `type:bug` - Bug fixes
- `type:chore` - Maintenance
- `type:research` - Research spikes

**Priority** (4):
- `priority:p0` - Critical
- `priority:p1` - High
- `priority:p2` - Medium
- `priority:p3` - Low

**Area** (2):
- `area:ui` - User interface
- `area:engine` - Core logic

**Note**: For single-repo apps, area labels are minimal. Add more as needed.

### .github-os.json

```json
{
  "projectName": "MyApp",
  "docsDir": "./docs",
  "repos": ["company/myapp"],
  "modules": [
    {
      "name": "main",
      "path": "./src",
      "type": "app",
      "description": "Main application"
    }
  ],
  "issueTracking": "github"
}
```

### Files to Create

1. `.github-os.json`
2. `.github/ISSUE_TEMPLATE/task.yml`
3. `.github/ISSUE_TEMPLATE/bug.yml`
4. `.github/ISSUE_TEMPLATE/feature.yml`
5. `.github/pull_request_template.md`

### Labels to Create (via GitHub MCP)

```javascript
// Type labels
mcp3_create_label({ owner: "company", repo: "myapp", name: "type:feature", color: "0e8a16", description: "New features" })
mcp3_create_label({ owner: "company", repo: "myapp", name: "type:bug", color: "d73a4a", description: "Bug fixes" })
mcp3_create_label({ owner: "company", repo: "myapp", name: "type:chore", color: "fef2c0", description: "Maintenance" })
mcp3_create_label({ owner: "company", repo: "myapp", name: "type:research", color: "d4c5f9", description: "Research spikes" })

// Priority labels
mcp3_create_label({ owner: "company", repo: "myapp", name: "priority:p0", color: "b60205", description: "Critical" })
mcp3_create_label({ owner: "company", repo: "myapp", name: "priority:p1", color: "d93f0b", description: "High" })
mcp3_create_label({ owner: "company", repo: "myapp", name: "priority:p2", color: "fbca04", description: "Medium" })
mcp3_create_label({ owner: "company", repo: "myapp", name: "priority:p3", color: "0e8a16", description: "Low" })

// Area labels
mcp3_create_label({ owner: "company", repo: "myapp", name: "area:ui", color: "1d76db", description: "UI/UX" })
mcp3_create_label({ owner: "company", repo: "myapp", name: "area:engine", color: "5319e7", description: "Core logic" })
```

### Sample Issue

**Title**: Implement user authentication

**Labels**: `type:feature`, `priority:p1`, `area:engine`

**Body**:
```markdown
## Summary
Add email/password authentication for user accounts

## Context

### Documentation
- Architecture: ./docs/architecture.md#auth-system
- ADR: ./docs/ADRs/0003-auth-strategy.md (to be created)
- Current task: ./docs/current-task.md

### Related
- Related: None (new feature)

## Scope

### In Scope
- User registration endpoint
- Login endpoint
- Password hashing
- Session management
- JWT token generation

### Out of Scope
- OAuth/SSO (separate feature)
- Password reset (separate feature)
- 2FA (separate feature)

### Files
- src/services/auth.ts (new)
- src/services/user.ts (modify)
- src/utils/jwt.ts (new)
- tests/services/auth.test.ts (new)

## Goal
Users can register accounts and log in with email/password

## Constraints
- Use bcrypt for password hashing
- JWT tokens expire in 7 days
- Session storage in Redis
- Follow existing error handling patterns

## Acceptance Criteria
- [ ] User can register with email/password
- [ ] Duplicate emails rejected
- [ ] User can login with correct credentials
- [ ] Invalid credentials rejected
- [ ] JWT token issued on successful login
- [ ] Token validated on protected endpoints
- [ ] Unit tests >80% coverage
- [ ] Integration tests pass
```
