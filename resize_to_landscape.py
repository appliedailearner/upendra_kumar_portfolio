import os
from PIL import Image

# Configuration
TARGET_WIDTH = 1024
TARGET_HEIGHT = 576
BG_COLOR = (30, 41, 59) # #1e293b (Dark Slate)
IMG_DIR = r"C:\MyResumePortfolio\images\blog\2026-01-15"

def process_images():
    if not os.path.exists(IMG_DIR):
        print(f"Directory not found: {IMG_DIR}")
        return

    for filename in os.listdir(IMG_DIR):
        if filename.lower().endswith(".png"):
            filepath = os.path.join(IMG_DIR, filename)
            try:
                with Image.open(filepath) as img:
                    # Skip if already 16:9 (approx)
                    ratio = img.width / img.height
                    if 1.7 < ratio < 1.8:
                        print(f"Skipping {filename} (Already 16:9)")
                        continue

                    print(f"Processing {filename}...")
                    
                    # 1. Resize original to fit within target height
                    # Ratio is 1:1, so new dims will be (TARGET_HEIGHT, TARGET_HEIGHT) = (576, 576)
                    scale_factor = TARGET_HEIGHT / img.height
                    new_size = (int(img.width * scale_factor), TARGET_HEIGHT)
                    
                    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                    
                    # 2. Create new canvas
                    canvas = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), BG_COLOR)
                    
                    # 3. Paste centered
                    x_offset = (TARGET_WIDTH - new_size[0]) // 2
                    canvas.paste(resized_img, (x_offset, 0))
                    
                    # 4. Save (overwrite)
                    canvas.save(filepath)
                    print(f"Done: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    process_images()
