const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const ROOT_DIR = 'C:\\MyResumePortfolio';
const EXCLUDE_DIR = 'toolkit';
const IMAGE_EXTS = ['.png', '.jpg', '.jpeg'];

// Helper to walk directory
function* walkSync(dir) {
    const files = fs.readdirSync(dir, { withFileTypes: true });
    for (const file of files) {
        if (file.isDirectory()) {
            yield* walkSync(path.join(dir, file.name));
        } else {
            yield path.join(dir, file.name);
        }
    }
}

async function convertImages() {
    console.log('Starting image conversion...');
    const imagesToProcess = [];

    for (const filePath of walkSync(ROOT_DIR)) {
        if (filePath.includes(EXCLUDE_DIR) || filePath.includes('node_modules') || filePath.includes('.git')) continue;

        const ext = path.extname(filePath).toLowerCase();
        if (IMAGE_EXTS.includes(ext)) {
            imagesToProcess.push(filePath);
        }
    }

    console.log(`Found ${imagesToProcess.length} images to process.`);
    const conversions = [];

    for (const imgPath of imagesToProcess) {
        const dir = path.dirname(imgPath);
        const name = path.parse(imgPath).name;
        const webpPath = path.join(dir, name + '.webp');

        if (!fs.existsSync(webpPath)) {
            conversions.push(
                sharp(imgPath)
                    .toFile(webpPath)
                    .then(() => {
                        console.log(`Converted: ${path.relative(ROOT_DIR, imgPath)} -> ${path.relative(ROOT_DIR, webpPath)}`);
                        return { original: imgPath, webp: webpPath };
                    })
                    .catch(err => console.error(`Failed to convert ${imgPath}:`, err))
            );
        } else {
            // Track it even if it exists so we can update HTML
            conversions.push(Promise.resolve({ original: imgPath, webp: webpPath }));
        }
    }

    const results = await Promise.all(conversions);
    return results.filter(r => r);
}

function updateReferences(convertedFiles) {
    console.log('Updating references in HTML/MD files...');
    const filesToUpdate = [];

    for (const filePath of walkSync(ROOT_DIR)) {
        if (filePath.includes('node_modules') || filePath.includes('.git')) continue;
        const ext = path.extname(filePath).toLowerCase();
        if (['.html', '.md'].includes(ext)) {
            filesToUpdate.push(filePath);
        }
    }

    let totalReplacements = 0;

    for (const filePath of filesToUpdate) {
        let content = fs.readFileSync(filePath, 'utf8');
        let fileChanged = false;

        // Create a map of filename -> webp filename for replacements
        // We replace strict filename matches to avoid path issues if possible, 
        // but robustly we should verify the relative path. 
        // For simplicity in this static site, often just replacing extension works if the filename is unique enough.
        // Let's use a regex replace for known extensions.

        // Strategy: Look for standard image references.
        // src=".../image.png" -> src=".../image.webp"

        // We iterate over the converted files to ensure we only replace existing WebP targets
        for (const { original } of convertedFiles) {
            const baseName = path.basename(original);
            const ext = path.extname(original);
            const name = path.parse(original).name;
            const webpName = name + '.webp';

            // Regex to match the filename locally in attributes
            // Matches: src="...foo.png", href="...foo.png", url('...foo.png')
            // We use a global replace
            if (content.includes(baseName)) {
                // Check if it's NOT in a toolkit path in the content (unlikely, but good to check context)
                // actually we just replace the extension for that specific file occurrence
                const regex = new RegExp(baseName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
                content = content.replace(regex, webpName);
                fileChanged = true;
                totalReplacements++;
            }
        }

        if (fileChanged) {
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`Updated references in: ${path.relative(ROOT_DIR, filePath)}`);
        }
    }
    console.log(`Total references updated: ${totalReplacements}`);
}

async function main() {
    try {
        const converted = await convertImages();
        updateReferences(converted);
        console.log('Done.');
    } catch (e) {
        console.error('Script failed:', e);
        process.exit(1);
    }
}

main();
