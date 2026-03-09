---
type: lesson
scope: global
tags: [async, error-handling, node, promises]
date: 2024-03-15
severity: high
---

# Unhandled Promise Rejection in Background Job Processor

## 1. Context

Implementing a background job processing system for sending email notifications in a Node.js application. The system processes batches of 100 emails concurrently using `Promise.all()` to maximize throughput.

**Initial approach**:
- Used `Promise.all()` to process email batches in parallel
- Assumed all promises would resolve successfully
- No explicit error handling around the parallel operations
- Running on Node.js 16 with default unhandled rejection behavior

**Technologies involved**:
- Node.js 16.x
- Custom EmailService using nodemailer
- Redis queue for job management

## 2. Mistake

The application crashed in production with the following error:

```
(node:1234) UnhandledPromiseRejectionWarning: Error: SMTP connection failed
    at SMTPConnection.connect (/app/node_modules/nodemailer/lib/smtp-connection/index.js:543)
    at EmailService.sendEmail (/app/services/email.js:42)
(node:1234) UnhandledPromiseRejectionWarning: Unhandled promise rejection. 
This error originated either by throwing inside of an async function without a catch block, 
or by rejecting a promise which was not handled with .catch().
```

**Observable symptoms**:
- Server process terminated unexpectedly
- 78 out of 100 emails in the batch were never sent
- No error logs captured in application monitoring
- Job queue left in inconsistent state (job marked as processing but never completed)

**Impact**:
- Production outage (15 minutes downtime)
- Customer notifications delayed
- Had to manually identify and requeue failed jobs
- Lost visibility into which specific emails failed

## 3. Root Cause

The code used `Promise.all()` within an async function but **forgot to await it**, meaning the promise rejection was not caught by the surrounding try-catch block:

```javascript
// The problematic code
async function processEmailBatch(emails) {
  try {
    // ❌ MISTAKE: Not awaiting Promise.all()
    Promise.all(
      emails.map(email => emailService.sendEmail(email))
    );
    
    await jobQueue.markComplete(batchId);
    return { success: true };
  } catch (error) {
    // This catch block never executed because Promise.all() wasn't awaited
    logger.error('Batch failed:', error);
    await jobQueue.markFailed(batchId);
  }
}
```

**Why this happened**:
1. Promise.all() returns a promise, but without `await`, execution continued immediately
2. The try-catch block completed successfully before any email actually sent
3. When the SMTP connection failed, the rejection occurred outside the try-catch scope
4. Node.js 16+ terminates the process on unhandled promise rejections by default

**Why it wasn't immediately obvious**:
- In development, SMTP always succeeded (localhost mail server)
- Unit tests mocked the email service and didn't test failure scenarios
- The code "looked correct" with a try-catch block present
- No linter warnings about missing await (need specific ESLint rules)

## 4. Correction

Added `await` before `Promise.all()` and implemented proper error handling for partial failures:

```javascript
// ✅ CORRECTED: Await Promise.all() and handle partial failures
async function processEmailBatch(emails) {
  try {
    // Await the promise and handle individual failures
    const results = await Promise.allSettled(
      emails.map(async (email) => {
        try {
          await emailService.sendEmail(email);
          return { email: email.to, status: 'sent' };
        } catch (error) {
          logger.warn('Email failed:', { email: email.to, error: error.message });
          return { email: email.to, status: 'failed', error: error.message };
        }
      })
    );
    
    const succeeded = results.filter(r => r.value?.status === 'sent').length;
    const failed = results.filter(r => r.value?.status === 'failed').length;
    
    logger.info('Batch complete:', { succeeded, failed, total: emails.length });
    
    // Mark job complete with stats
    await jobQueue.markComplete(batchId, { succeeded, failed });
    
    return { 
      success: true, 
      stats: { succeeded, failed, total: emails.length },
      failures: results.filter(r => r.value?.status === 'failed').map(r => r.value)
    };
    
  } catch (error) {
    // This now catches any unexpected errors in the batch processing logic itself
    logger.error('Batch processing error:', error);
    await jobQueue.markFailed(batchId, error.message);
    throw error; // Re-throw for caller to handle
  }
}
```

**Additional changes**:
1. **Switched to `Promise.allSettled()`**: Allows partial batch success instead of all-or-nothing
2. **Individual error handling**: Each email send is wrapped in try-catch to log specific failures
3. **Detailed stats tracking**: Return counts of succeeded/failed emails
4. **Better logging**: Warn-level for individual failures, error-level for batch failures
5. **Added ESLint rule**: Configured `no-floating-promises` rule to catch future occurrences

**Testing improvements**:
```javascript
// Added integration test for SMTP failures
it('should handle partial batch failures gracefully', async () => {
  const emails = [
    { to: 'success@example.com', subject: 'Test 1' },
    { to: 'fail@example.com', subject: 'Test 2' }, // Will fail
    { to: 'success2@example.com', subject: 'Test 3' }
  ];
  
  // Mock SMTP to fail for specific email
  emailService.sendEmail.mockImplementation((email) => {
    if (email.to === 'fail@example.com') {
      return Promise.reject(new Error('SMTP connection failed'));
    }
    return Promise.resolve();
  });
  
  const result = await processEmailBatch(emails);
  
  expect(result.stats.succeeded).toBe(2);
  expect(result.stats.failed).toBe(1);
  expect(result.failures[0].email).toBe('fail@example.com');
});
```

## 5. Prevention Rule

**Always await `Promise.all()` or `Promise.allSettled()` within try-catch blocks in async functions.**

**Verification in code review**:
- ✅ Search for `Promise.all(` and verify `await` appears directly before it
- ✅ Confirm the await is inside a try-catch or the function has `.catch()` chained
- ✅ Check ESLint configuration includes `@typescript-eslint/no-floating-promises`

**When to apply**:
- ANY use of `Promise.all()` in async functions
- Parallel promise operations that may fail
- Background jobs or batch processing

**Examples**:

✅ **Good** - Awaited with error handling:
```javascript
try {
  await Promise.all(promises);
} catch (error) {
  handleError(error);
}
```

✅ **Good** - Using allSettled for partial success:
```javascript
const results = await Promise.allSettled(promises);
const failures = results.filter(r => r.status === 'rejected');
```

❌ **Bad** - Not awaited (floating promise):
```javascript
async function process() {
  try {
    Promise.all(promises); // ❌ Not awaited!
    console.log('Done'); // Logs before promises complete
  } catch (error) {
    // Never catches promise rejections
  }
}
```

❌ **Bad** - Awaited but no error handling:
```javascript
async function process() {
  await Promise.all(promises); // ❌ No try-catch
  // Rejection propagates up, may become unhandled
}
```

**Additional recommendations**:
- Enable `no-floating-promises` in ESLint/TSLint
- Use `Promise.allSettled()` when partial success is acceptable
- Always log individual failures in batch operations
- Test failure scenarios, not just happy paths
