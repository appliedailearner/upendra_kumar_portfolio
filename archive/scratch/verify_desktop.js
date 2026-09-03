const { chromium } = require('playwright-chromium');
const path = require('path');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1280, height: 800 });

    const localPath = 'C:\\MyResumePortfolio';
    const newFile = 'file:///' + path.join(localPath, 'index.html').replace(/\\/g, '/');

    console.log(`Capturing New Version (Desktop): ${newFile}`);
    try {
        await page.goto(newFile, { waitUntil: 'networkidle' });
        // Wait a bit extra to let layout settle
        await page.waitForTimeout(1000);
        await page.screenshot({ path: path.join(localPath, 'new_version_desktop.png'), fullPage: true });
        console.log('Desktop screenshot saved successfully.');
    } catch (e) {
        console.error('Error:', e.message);
    }
    await browser.close();
})();
