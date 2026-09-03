const { chromium } = require('playwright-chromium');

(async () => {
    const browser = await chromium.launch();

    // Check GitHub Pages
    console.log('Testing GitHub Pages...');
    const page1 = await browser.newPage();
    await page1.goto('https://appliedailearner.github.io/upendra_kumar_portfolio/blog/2026-03-18-why-the-future-of-azure-architecture-is-programmable.html', { waitUntil: 'networkidle' });

    // Scroll down to the matrix to ensure it's in view and rendered properly
    await page1.evaluate(() => {
        window.scrollBy(0, document.body.scrollHeight / 2);
    });
    // wait a bit for any scroll animations
    await page1.waitForTimeout(1000);

    await page1.screenshot({ path: 'c:\\MyResumePortfolio\\validation_github.png', fullPage: true });
    console.log('GitHub screenshot saved.');
    await page1.close();

    // Check Azure Blob Storage
    console.log('Testing Azure Blob Storage...');
    const page2 = await browser.newPage();
    await page2.goto('https://porfolioupendrakumar.z29.web.core.windows.net/blog/2026-03-18-why-the-future-of-azure-architecture-is-programmable.html', { waitUntil: 'networkidle' });

    await page2.evaluate(() => {
        window.scrollBy(0, document.body.scrollHeight / 2);
    });
    await page2.waitForTimeout(1000);

    await page2.screenshot({ path: 'c:\\MyResumePortfolio\\validation_azure.png', fullPage: true });
    console.log('Azure screenshot saved.');
    await page2.close();

    await browser.close();
    console.log('Validation complete.');
})();
