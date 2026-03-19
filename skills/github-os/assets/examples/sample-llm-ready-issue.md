# Sample LLM-Ready Issue

This is an example of a fully LLM-ready issue that meets all criteria.

---

**Title**: Implement password reset flow

**Labels**: 
- `type:feature`
- `priority:p1`
- `module:api`
- `status:llm-ready`

**Assignee**: (none - ready to pick up)

---

## Summary
Add password reset functionality allowing users to reset forgotten passwords via email

## Context

### Documentation
- **Architecture**: `./docs/architecture.md#authentication-system`
  - Section 4.2: Email service integration
  - Section 4.3: Token management
- **ADRs**: 
  - `./docs/ADRs/0015-email-provider.md` (SendGrid implementation)
  - `./docs/ADRs/0018-token-expiration.md` (Security tokens expire in 1 hour)
- **Current task**: `./docs/current-task.md` (updated with context)

### Related Issues
- **Depends on**: None (all dependencies resolved)
- **Blocks**: #89 (User settings page - needs reset link)
- **Related**: #42 (Email verification - similar email flow pattern)

### Code Context
- Email service already implemented (SendGrid)
- Token generation utility exists (`src/utils/tokens.ts`)
- User model has email field validated
- Database has `password_reset_tokens` table

## Scope

### In Scope
1. **API Endpoints**:
   - `POST /auth/password-reset/request` - Request reset email
   - `POST /auth/password-reset/confirm` - Confirm reset with token

2. **Email**:
   - Password reset email template
   - Secure reset link with token

3. **Security**:
   - Token generation (cryptographically secure)
   - Token expiration (1 hour)
   - Rate limiting (max 3 requests per hour per email)
   - Token single-use enforcement

4. **Validation**:
   - Email existence check
   - Token validity check
   - Password strength requirements

### Out of Scope
- UI/Frontend components (separate issue #90)
- Account recovery without email (future feature)
- SMS-based reset (future feature)
- Multi-factor authentication (separate epic #50)

### Files Affected

**New Files**:
- `src/routes/auth/password-reset.ts` - Route handlers
- `src/services/password-reset.ts` - Business logic
- `src/templates/emails/password-reset.html` - Email template
- `tests/routes/auth/password-reset.test.ts` - API tests
- `tests/services/password-reset.test.ts` - Service tests

**Modified Files**:
- `src/routes/auth/index.ts` - Add password reset routes
- `src/models/User.ts` - Add resetPassword method
- `src/services/email.ts` - Add password reset email method
- `database/migrations/NNNN_password_reset_tokens.ts` - Already exists ✓

## Goal

Users who forget their password can:
1. Request a password reset via email
2. Receive a secure reset link
3. Set a new password using the link
4. Successfully log in with the new password

## Constraints

### Technical
- **Token**: Use `crypto.randomBytes(32)` for token generation
- **Hashing**: Use bcrypt for new password (same as registration)
- **Storage**: Store tokens in `password_reset_tokens` table
- **Email**: Use existing SendGrid integration
- **Rate limiting**: Use existing rate limiter middleware

### Security
- Tokens must expire in 1 hour (per ADR-0018)
- Tokens must be single-use only
- No user enumeration (always return success even if email doesn't exist)
- Constant-time comparison for tokens
- HTTPS required in production

### Performance
- Email sent asynchronously (don't block response)
- Database queries optimized with indexes
- Token lookup by indexed token column

### Style
- Follow existing auth route patterns (see `src/routes/auth/login.ts`)
- Error messages match existing auth errors
- Logging matches existing auth logging format

## Acceptance Criteria

### Functionality
- [ ] Request endpoint accepts email, returns success
- [ ] Reset email sent with secure token link
- [ ] Confirm endpoint validates token and updates password
- [ ] Old password no longer works after reset
- [ ] New password works for login
- [ ] Expired tokens rejected (after 1 hour)
- [ ] Used tokens rejected (single-use)
- [ ] Invalid tokens rejected
- [ ] Rate limiting enforced (3 requests/hour/email)
- [ ] Non-existent emails handled without enumeration

### Testing
- [ ] Unit tests for password reset service (>80% coverage)
- [ ] Integration tests for request endpoint
- [ ] Integration tests for confirm endpoint
- [ ] Test token expiration handling
- [ ] Test token reuse prevention
- [ ] Test rate limiting
- [ ] Test email delivery (mocked SendGrid)
- [ ] All tests pass in CI

### Documentation
- [ ] API documentation updated (`./docs/api/auth.md`)
- [ ] Email template reviewed for clarity
- [ ] Security considerations documented
- [ ] Error codes documented

### Security Review
- [ ] No user enumeration vulnerability
- [ ] Token generation cryptographically secure
- [ ] Token storage secure
- [ ] Rate limiting effective
- [ ] Email link uses HTTPS in production

## Implementation Notes

### Email Template Structure
```html
Subject: Reset your password

Hi there,

You requested a password reset. Click the link below to set a new password:

[Reset Password Button - links to: https://app.example.com/reset?token=ABC123]

This link expires in 1 hour.

If you didn't request this, ignore this email.
```

### Database Schema (already exists)
```sql
CREATE TABLE password_reset_tokens (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  token VARCHAR(64) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP NOT NULL,
  used_at TIMESTAMP NULL,
  INDEX idx_token (token),
  INDEX idx_expires (expires_at)
);
```

### API Response Format
```json
POST /auth/password-reset/request
Request: { "email": "user@example.com" }
Response: { "success": true, "message": "If that email exists, a reset link was sent" }

POST /auth/password-reset/confirm
Request: { "token": "abc123", "newPassword": "SecurePass123!" }
Response: { "success": true, "message": "Password updated successfully" }
```

### Error Codes
- `INVALID_TOKEN` - Token not found or invalid format
- `EXPIRED_TOKEN` - Token has expired
- `USED_TOKEN` - Token already used
- `WEAK_PASSWORD` - Password doesn't meet requirements
- `RATE_LIMITED` - Too many reset requests

## Why This is LLM-Ready

✅ **Clear Goal**: Single, specific feature defined  
✅ **Context Linked**: Architecture + 2 ADRs + related issues  
✅ **Scope Defined**: Exact files listed, in/out scope explicit  
✅ **Acceptance Criteria**: 20+ testable conditions  
✅ **No Blockers**: All dependencies resolved  
✅ **Files Identified**: 9 files with new/modify tags  
✅ **Constraints Listed**: Technical, security, performance, style  
✅ **Implementation Notes**: Concrete examples provided  

An LLM can pick this up and implement it without additional questions.
