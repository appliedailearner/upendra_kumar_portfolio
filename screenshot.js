const { chromium } = require('playwright-chromium');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    // Capture console messages
    page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
    page.on('pageerror', err => console.log('BROWSER ERR:', err.message));

    await page.goto('https://portfolio.upendrakumar.com/blog/2026-01-29-architectural-integrity-ai-audit-framework.html', { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'c:\\MyResumePortfolio\\blog_audit_screenshot.png', fullPage: true });
    console.log('Screenshot saved to c:\\MyResumePortfolio\\blog_audit_screenshot.png');
    await browser.close();
})();
