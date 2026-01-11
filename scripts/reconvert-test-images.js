const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const images = [
    'test-0',
    'test-1',
    'test-2'
];

const basePath = 'C:/MyResumePortfolio/assets/diagrams/png_hi';

(async () => {
    for (const imgVerified of images) {
        const input = path.join(basePath, imgVerified + '.png');
        const output = path.join(basePath, imgVerified + '.webp');

        try {
            console.log(`Processing: ${input}`);
            await sharp(input)
                .webp({ lossless: true })
                .toFile(output);
            console.log(`Successfully converted: ${output}`);
        } catch (err) {
            console.error(`Error converting ${input}:`, err);
        }
    }
})();
