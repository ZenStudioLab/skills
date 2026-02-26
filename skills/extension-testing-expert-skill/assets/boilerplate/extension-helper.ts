import { test as base, chromium, type BrowserContext, type Page } from '@playwright/test';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// ADJUST THIS PATH: Point to your extension's build output (e.g., .output/chrome-mv3)
const EXTENSION_PATH = path.resolve(__dirname, '../../.output/chrome-mv3');

/**
 * Extension E2E Setup Helper
 * 
 * This helper initializes a persistent browser context with the built extension loaded.
 * It provides the extension ID for navigating to popup or options pages.
 */
export const test = base.extend<{
    context: BrowserContext;
    extensionId: string;
    optionsPage: Page;
}>({
    context: async ({ }, use, testInfo) => {
        const pathToExtension = EXTENSION_PATH;
        // Use a unique directory per worker to avoid profile lock issues
        const userDataDir = path.resolve(__dirname, `../../.test-user-data-${testInfo.workerIndex}`);

        const context = await chromium.launchPersistentContext(userDataDir, {
            headless: false, // Extensions require non-headless mode for full functionality
            args: [
                `--disable-extensions-except=${pathToExtension}`,
                `--load-extension=${pathToExtension}`,
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ],
        });
        await use(context);
        await context.close();
    },
    extensionId: async ({ context }, use) => {
        // For MV3, the extension ID is used to navigate to pages
        console.log('Waiting for service worker...');
        let [background] = context.serviceWorkers();
        if (!background) {
            try {
                background = await context.waitForEvent('serviceworker', { timeout: 20000 });
            } catch (e) {
                console.log('Service worker event timeout, checking current workers...');
                [background] = context.serviceWorkers();
            }
        }

        if (!background) throw new Error('Extension background service worker not found');

        // Clear extension storage before each test (global setup)
        console.log('Clearing extension storage...');
        await background.evaluate(async () => {
            await chrome.storage.local.clear();
            await chrome.storage.sync.clear();
        });
        console.log('Extension storage cleared.');
        
        // Wait for state to sync after storage clear
        await new Promise(resolve => setTimeout(resolve, 2000));

        const extensionId = background.url().split('/')[2];
        console.log('Extension ID:', extensionId);
        await use(extensionId);
    },
    optionsPage: async ({ context, extensionId }, use) => {
        console.log('Navigating to options page...');
        const page = await context.newPage();

        // Add browser logging
        page.on('console', msg => {
            if (msg.type() === 'error' || msg.type() === 'warning' || msg.type() === 'log') {
                console.log(`BROWSER ${msg.type().toUpperCase()}:`, msg.text());
            }
        });

        // ADJUST THIS URL: Point to your extension's primary entrypoint
        const url = `chrome-extension://${extensionId}/options.html`;
        console.log('URL:', url);
        await page.goto(url, { waitUntil: 'load' });
        console.log('Options page loaded.');

        // Wait for page to be truly ready before dismissing
        await page.waitForTimeout(3000);
        await dismissWelcomeBanner(page);

        await use(page);
        await page.close();
    },
});

export const expect = test.expect;

/**
 * Common interaction helpers
 */
export async function dismissWelcomeBanner(page: any) {
    const welcomeButtons = page.locator('button:has-text("Get Started"), button:has-text("Dismiss"), button:has-text("Got it"), button:has-text("Grant Access")');

    try {
        let dismissedCount = 0;
        const maxRetries = 5;

        while (dismissedCount < maxRetries) {
            await page.waitForTimeout(3000);
            const count = await welcomeButtons.count();
            if (count === 0) {
                const isDialogOpen = await page.locator('.MuiDialog-root').isVisible().catch(() => false);
                if (!isDialogOpen) break;
                await page.waitForTimeout(1000);
                if (await welcomeButtons.count() === 0) break;
            }

            console.log(`Found ${count} onboarding button(s). Dismissing layer ${dismissedCount + 1}...`);
            for (let i = 0; i < count; i++) {
                try {
                    const btn = welcomeButtons.nth(i);
                    if (await btn.isVisible()) {
                        await btn.click({ force: true, timeout: 3000 });
                        await page.waitForTimeout(1000);
                    }
                } catch (e) { }
            }

            await page.waitForSelector('.MuiDialog-root', { state: 'hidden', timeout: 5000 }).catch(() => { });
            dismissedCount++;
        }
    } catch (e) {
        console.log('Onboarding dismissal failed:', e);
    }
}
