import { defineConfig, devices } from '@playwright/test';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ADJUST THIS PATH: Point to your extension's build output (e.g., .output/chrome-mv3)
const EXTENSION_PATH = path.resolve(__dirname, '.output/chrome-mv3');

/**
 * Extension E2E Test Configuration
 * 
 * Browser extensions require a persistent context and cannot run headless.
 * The extension must be built BEFORE running E2E tests.
 */
export default defineConfig({
    testDir: './tests/e2e',
    /* Extensions share a persistent context - run sequentially to avoid state collisions */
    fullyParallel: false,
    /* Fail the build on CI if you accidentally left test.only in the source code. */
    forbidOnly: !!process.env.CI,
    /* Retry on CI only */
    retries: process.env.CI ? 2 : 0,
    /* Keep workers low to avoid multiple browser instances conflicting with the same profile */
    workers: 1,
    reporter: 'html',
    use: {
        /* Collect trace when retrying the failed test. */
        trace: 'on-first-retry',
        screenshot: 'only-on-failure',

        // Mandatory: Extensions require non-headless mode for proper functionality
        headless: false,
    },

    /* Configure projects for major browsers */
    projects: [
        {
            name: 'chromium',
            use: {
                ...devices['Desktop Chrome'],
            }
        }
    ],
});
