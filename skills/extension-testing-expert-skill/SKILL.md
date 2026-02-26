---
name: playwright-extension-testing
description: "Expert guidance for writing and running end-to-end (E2E) tests for browser extensions using Playwright. Use when: (1) Setting up E2E testing for a new extension project, (2) Adding new test cases to an existing extension, (3) Debugging flaky extension tests, (4) Optimizing CI/CD pipelines for extension testing (e.g., XVFB setup)."
---

# Playwright Extension Testing Expert

This skill provides a "gold standard" for browser extension E2E testing, specifically optimized for MV3 and frameworks like WXT. Extensions require unique handling for persistent browser contexts, non-headless modes, and onboarding flows.

## Core Mandates

1. **Non-Headless is Mandatory:** Browser extensions do NOT load properly in standard headless mode. Use `headless: false`.
2. **Persistent Context:** Extensions require `launchPersistentContext` to maintain state and load correctly.
3. **XVFB for Linux/CI:** Always prefix test commands with `xvfb-run -a` on Linux/CI to provide a virtual display for the non-headless browser.
4. **Data-TestId First:** Prohibit text-based locators. Always add `data-testid` to source code if missing.
5. **Dismiss Onboarding:** Every test must dismiss welcome banners/onboarding dialogs before interacting with the UI.
6. **Complementary Usage:** This skill is highly specialized for extensions. For general Playwright best practices (locators, assertions, reporting), you MUST check if `playwright-expert` or `playwright-skill` is available and use them in tandem.

## Available Boilerplate (Assets)

This skill provides pre-configured boilerplate to jumpstart a project. See the `assets/boilerplate/` directory.

- **`extension-helper.ts`**: A robust Playwright fixture setup including `extensionId` discovery and onboarding dismissal.
- **`playwright.config.ts`**: The recommended configuration for extension testing.

## Workflow: Setting Up a New Project

1. **Identify Project Structure:** Determine where the built extension output is located (e.g., `.output/chrome-mv3`).
2. **Inject Boilerplate:** Use the `read_file` tool to extract the boilerplate from this skill's `assets/` and write them to the target project's `tests/e2e/` directory.
3. **Verify Build Step:** Remind the user that extensions must be built BEFORE running E2E tests (`yarn build`).
4. **Run First Test:** Use `xvfb-run -a playwright test` to verify the setup.

## Best Practices

### The "Dismissal" Loop
Always use the `dismissWelcomeBanner` helper provided in the boilerplate. Extensions often have multiple layers of onboarding (e.g., "Grant Access", "Get Started").

### Storage Management
The boilerplate's `extensionId` fixture automatically clears `chrome.storage.local` and `chrome.storage.sync` before each test. Ensure tests don't assume state exists unless they create it.

### Waiting for UI Settle
Extensions can be slower to load than standard web pages. Use a `3000ms` settle time after navigation or dismissal.
