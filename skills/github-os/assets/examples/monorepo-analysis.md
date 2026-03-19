# Repository Analysis Example: Monorepo

## Input

**Repository**: `company/platform`

**Structure**:
```
platform/
├── apps/
│   ├── web/
│   │   ├── src/
│   │   └── package.json
│   └── mobile/
│       ├── src/
│       └── package.json
├── services/
│   ├── api/
│   │   ├── src/
│   │   └── package.json
│   └── worker/
│       ├── src/
│       └── package.json
├── packages/
│   ├── ui/
│   │   ├── src/
│   │   └── package.json
│   └── utils/
│       ├── src/
│       └── package.json
├── docs/
│   ├── architecture.md
│   └── ADRs/
├── package.json (workspace root)
├── pnpm-workspace.yaml
└── turbo.json
```

## Analysis Output

### Repository Type
**Monorepo**

**Build System**: Turborepo (detected via `turbo.json`)

**Package Manager**: pnpm (detected via `pnpm-workspace.yaml`)

### Modules Detected

1. **web** (type: app, path: ./apps/web)
2. **mobile** (type: app, path: ./apps/mobile)
3. **api** (type: service, path: ./services/api)
4. **worker** (type: service, path: ./services/worker)
5. **ui** (type: package, path: ./packages/ui)
6. **utils** (type: package, path: ./packages/utils)

### Documentation Structure
- **Docs directory**: `./docs`
- **Architecture docs**: ✅ Found (`./docs/architecture.md`)
- **ADRs**: ✅ Found (`./docs/ADRs/`)
- **Assessment**: Rich

### Execution Surfaces
- **Primary repo**: company/platform
- **Total modules**: 6
- **Recommended label count**: 18
  - 4 type labels
  - 4 priority labels
  - 4 area labels
  - 6 module labels

## GitHub OS Design

### Labels (18 total)

**Type** (4):
- `type:feature`
- `type:bug`
- `type:chore`
- `type:research`

**Priority** (4):
- `priority:p0`
- `priority:p1`
- `priority:p2`
- `priority:p3`

**Area** (4):
- `area:ui`
- `area:engine`
- `area:infra`
- `area:dx`

**Module** (6):
- `module:web` - Web application
- `module:mobile` - Mobile application
- `module:api` - REST API service
- `module:worker` - Background worker
- `module:ui` - UI component library
- `module:utils` - Utility library

### .github-os.json

```json
{
  "projectName": "Platform",
  "docsDir": "./docs",
  "repos": ["company/platform"],
  "modules": [
    {
      "name": "web",
      "path": "./apps/web",
      "type": "app",
      "description": "Web application (React + Next.js)"
    },
    {
      "name": "mobile",
      "path": "./apps/mobile",
      "type": "app",
      "description": "Mobile application (React Native)"
    },
    {
      "name": "api",
      "path": "./services/api",
      "type": "service",
      "description": "REST API service (Node.js + Express)"
    },
    {
      "name": "worker",
      "path": "./services/worker",
      "type": "service",
      "description": "Background worker (Bull + Redis)"
    },
    {
      "name": "ui",
      "path": "./packages/ui",
      "type": "package",
      "description": "Shared UI component library"
    },
    {
      "name": "utils",
      "path": "./packages/utils",
      "type": "package",
      "description": "Shared utility functions"
    }
  ],
  "issueTracking": "github",
  "labels": {
    "customAreas": ["payments", "notifications"]
  },
  "githubProject": {
    "url": "https://github.com/orgs/company/projects/1",
    "id": 1
  }
}
```

### Labels to Create (18 via GitHub MCP)

```bash
# Type labels (4)
type:feature, type:bug, type:chore, type:research

# Priority labels (4)
priority:p0, priority:p1, priority:p2, priority:p3

# Area labels (4)
area:ui, area:engine, area:infra, area:dx

# Module labels (6)
module:web, module:mobile, module:api, module:worker, module:ui, module:utils
```

### Sample Cross-Module Issue

**Title**: Add user profile photo upload

**Labels**: `type:feature`, `priority:p1`, `module:api`, `module:web`, `module:mobile`

**Body**:
```markdown
## Summary
Enable users to upload profile photos

## Context

### Documentation
- Architecture: ./docs/architecture.md#file-uploads
- ADR: ./docs/ADRs/0025-s3-storage.md
- Current task: ./docs/current-task.md

### Related
- Blocks: #156 (Profile page redesign)
- Related: #142 (Image optimization)

## Scope

### In Scope
**API** (module:api):
- Upload endpoint (multipart/form-data)
- S3 integration
- Image validation
- URL generation

**Web** (module:web):
- Upload UI component
- Image cropper
- Preview
- Error handling

**Mobile** (module:mobile):
- Camera/gallery picker
- Upload progress
- Preview
- Error handling

### Out of Scope
- Video uploads (future)
- Multiple photos (future)
- Photo albums (separate feature)

### Files
**services/api**:
- src/routes/users/photo.ts (new)
- src/services/s3.ts (modify)
- tests/routes/users/photo.test.ts (new)

**apps/web**:
- src/components/ProfilePhoto.tsx (new)
- src/components/ImageCropper.tsx (new)

**apps/mobile**:
- src/screens/ProfileEdit.tsx (modify)
- src/components/PhotoPicker.tsx (new)

## Goal
Users can upload and display profile photos across web and mobile

## Constraints
- Max file size: 5MB
- Supported formats: JPG, PNG, WebP
- Auto-resize to 500x500px
- Store in S3 bucket: company-profile-photos
- CDN delivery via CloudFront

## Acceptance Criteria
- [ ] API endpoint accepts multipart upload
- [ ] Image validation (format, size)
- [ ] S3 upload working
- [ ] Web upload UI functional
- [ ] Web image cropper working
- [ ] Mobile camera/gallery picker working
- [ ] Profile photo displayed on web
- [ ] Profile photo displayed on mobile
- [ ] Error handling on all platforms
- [ ] Unit tests >80% coverage
- [ ] Integration tests pass
```

### GitHub Project Views

**By Module View**:
- Group by: Module
- Shows all work organized by app/service/package
- Easy to see what each team/area is working on

**Current Work View**:
- Filter: Status = "In Progress"
- Group by: Assignee
- Shows active work

**Cross-Module View**:
- Filter: Issues with 2+ module labels
- Shows work spanning multiple modules
- Requires coordination
