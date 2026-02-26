# Playwright Extension Testing Expert Skill

A portable, "gold standard" expert skill for writing and running end-to-end (E2E) tests for browser extensions using Playwright. 

This skill is designed to be used with AI agents (like Gemini CLI, Claude, or GitHub Copilot) to ensure they follow best practices for MV3 extension testing.

> [!TIP]
> This skill is highly specialized for browser extensions. For general Playwright best practices (locators, assertions, reporting), it is recommended to use this as a supplement to the broader `playwright-expert` or `playwright-skill`.

## 🚀 Features

- **MV3 Optimized:** Pre-configured for Manifest V3 and WXT.
- **Onboarding Dismissal:** Automatic handling of multi-layer welcome banners.
- **CI Ready:** Comprehensive guide for running non-headless tests on Linux/CI via XVFB.
- **Boilerplate Injection:** Ready-to-use fixtures for extension ID discovery and storage clearing.

## 📦 Project Structure

```text
playwright-extension-testing-skill/
├── SKILL.md            # The core instructions for AI agents
├── assets/
│   └── boilerplate/     # Gold-standard code templates
│       ├── extension-helper.ts
│       └── playwright.config.ts
└── references/
    └── xvfb-guide.md   # Linux/CI setup documentation
```

## 🛠️ How to Use

### For AI Agents (Gemini/Claude)
If you are using an agent that supports the "Skills" protocol (like Gemini CLI), you can activate this skill to instantly ground the agent in extension testing best practices.

**Trigger:** "I need to set up E2E tests for my browser extension."

### For Manual Use
You can manually copy the files from `assets/boilerplate` into your project's `tests/e2e` directory. 

1. Copy `extension-helper.ts` and `playwright.config.ts`.
2. Adjust the `EXTENSION_PATH` in both files to point to your build output.
3. Use `xvfb-run -a yarn playwright test` to run your tests.

## 📜 License
MIT
