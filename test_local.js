const { chromium } = require('playwright-chromium');
(async () => {
    const browser = await chromium.launch();
    console.log('Testing Local HTML...');
    const page = await browser.newPage();
    await page.goto('file:///C:/MyResumePortfolio/blog/2026-05-20-the-enterprise-ai-model-layer-azure-model-router.html', { waitUntil: 'networkidle' });
    
    await page.evaluate(() => {
        window.scrollBy(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(1000);
    
    await page.screenshot({ path: 'c:\\MyResumePortfolio\\validation_local.png', fullPage: true });
    console.log('Local screenshot saved.');
    await browser.close();
})();
