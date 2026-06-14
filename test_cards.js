const { chromium } = require('playwright-chromium');

(async () => {
    const browser = await chromium.launch();
    console.log('Testing Local HTML...');
    const page = await browser.newPage();
    
    await page.goto('file:///C:/MyResumePortfolio/blog/2026-05-20-the-enterprise-ai-model-layer-azure-model-router.html');
    
    // Auto-scroll to trigger lazy loading
    await page.evaluate(async () => {
        await new Promise((resolve) => {
            let totalHeight = 0;
            const distance = 300;
            const timer = setInterval(() => {
                const scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;
                if(totalHeight >= scrollHeight){
                    clearInterval(timer);
                    resolve();
                }
            }, 50);
        });
    });
    
    await page.waitForTimeout(1000);
    
    // Scroll back up to the middle where the workload mapping section is
    await page.evaluate(() => {
        window.scrollTo(0, 2000);
    });

    await page.waitForTimeout(500);

    await page.screenshot({ path: 'c:\\MyResumePortfolio\\validation_local_cards.png', fullPage: true });
    
    await browser.close();
    console.log('Test complete, screenshot saved.');
})();
