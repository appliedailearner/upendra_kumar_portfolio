const { chromium } = require('playwright-chromium');
const path = require('path');

async function generatePDF() {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    // Use the local file path directly
    const filePath = 'file://' + path.resolve(__dirname, '../pages/databricks-zero-trust-blueprint.html');

    console.log('Navigating to:', filePath);
    await page.goto(filePath, { waitUntil: 'networkidle' });

    // Wait for fonts to load
    await page.evaluateHandle('document.fonts.ready');

    console.log('Generating PDF...');
    await page.pdf({
        path: 'assets/databricks-zero-trust-blueprint.pdf',
        format: 'A4',
        printBackground: true,
        margin: {
            top: '0px',
            right: '0px',
            bottom: '0px',
            left: '0px'
        }
    });

    await browser.close();
    console.log('PDF generated successfully!');
}

generatePDF().catch(err => {
    console.error('Error generating PDF:', err);
    process.exit(1);
});
