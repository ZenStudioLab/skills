# Running Extension Tests on Linux/CI (XVFB)

Browser extensions require `headless: false` in Playwright to function correctly. This presents a challenge in CI/CD environments (like GitHub Actions) or on Linux servers without a GUI.

## The Solution: XVFB

XVFB (X Virtual Framebuffer) provides a virtual display for the browser to "render" into, even when no physical screen is present. This is also necesary, as with `headless: false`, Playwright will constantly spawn new browser instances for each test.

### 1. Install Dependencies

On Ubuntu/Debian:
```bash
sudo apt-get install -y xvfb
```

### 2. Run Tests with xvfb-run

Prefix your test command with `xvfb-run -a`. The `-a` flag automatically finds a free server number.

```bash
xvfb-run -a yarn playwright test
```

### 3. GitHub Actions Example

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: yarn install
      - run: yarn build
      - name: Run E2E Tests
        run: xvfb-run -a yarn playwright test
```

### Why `-a`?
Without `-a`, you might get "Display already in use" errors if multiple processes are running. `-a` ensures a clean environment for every test run.
