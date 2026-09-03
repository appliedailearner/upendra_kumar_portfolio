from PIL import Image, ImageChops
import os
import glob

def trim(im, padding=40):
    try:
        # Use top-left pixel as background color
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        if diff.mode == "RGBA":
            # If image has an alpha channel, getbbox() might be tricky.
            # Convert to RGB to find differences more reliably if the background is solid but has alpha.
            bg_rgb = Image.new("RGB", im.size, im.convert("RGB").getpixel((0,0)))
            diff = ImageChops.difference(im.convert("RGB"), bg_rgb)
        
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            width, height = im.size
            # Add padding
            left = max(0, bbox[0] - padding)
            upper = max(0, bbox[1] - padding)
            right = min(width, bbox[2] + padding)
            lower = min(height, bbox[3] + padding)
            
            # Only crop if we are actually reducing the size by a meaningful amount
            if left > 10 or upper > 10 or right < width - 10 or lower < height - 10:
                return im.crop((left, upper, right, lower))
    except Exception as e:
        print(f"Error during trim calculation: {e}")
    return im

def process_directory(directory):
    count = 0
    # Process the root directory images and all subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                filepath = os.path.join(root, file)
                try:
                    with Image.open(filepath) as img:
                        original_size = img.size
                        # Convert to handle different modes cleanly
                        trimmed_img = trim(img)
                        if trimmed_img.size != original_size:
                            trimmed_img.save(filepath)
                            print(f"Trimmed {filepath} from {original_size} to {trimmed_img.size}")
                            count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    print(f"Total images trimmed: {count}")

if __name__ == '__main__':
    # Process both the base blog dir for images and the assets dir
    process_directory('./blog')
