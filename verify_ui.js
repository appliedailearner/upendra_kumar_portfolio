const { chromium } = require('playwright-chromium');
const path = require('path');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    // Viewport size for varied testing
    await page.setViewportSize({ width: 1280, height: 800 });

    const localPath = 'C:\\MyResumePortfolio';
    const baselineFile = 'file:///' + path.join(localPath, 'index-test.html').replace(/\\/g, '/');
    const newFile = 'file:///' + path.join(localPath, 'index.html').replace(/\\/g, '/');

    console.log(`Capturing Baseline: ${baselineFile}`);
    try {
        await page.goto(baselineFile, { waitUntil: 'networkidle' });
        await page.screenshot({ path: path.join(localPath, 'baseline_screenshot.png'), fullPage: true });
        console.log('Baseline saved.');
    } catch (e) {
        console.error('Error capturing baseline:', e.message);
    }

    console.log(`Capturing New Version: ${newFile}`);
    try {
        await page.goto(newFile, { waitUntil: 'networkidle' });
        await page.screenshot({ path: path.join(localPath, 'new_version_screenshot.png'), fullPage: true });
        console.log('New version saved.');
    } catch (e) {
        console.error('Error capturing new version:', e.message);
    }

    // Mobile Viewport Check
    await page.setViewportSize({ width: 375, height: 667 });
    console.log(`Capturing New Version (Mobile): ${newFile}`);
    try {
        await page.goto(newFile, { waitUntil: 'networkidle' });
        await page.screenshot({ path: path.join(localPath, 'new_version_mobile.png'), fullPage: true });
        console.log('New version mobile saved.');
    } catch (e) {
        console.error('Error capturing mobile version:', e.message);
    }

    await browser.close();
})();
