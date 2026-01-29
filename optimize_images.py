import os
from PIL import Image

# Configuration
SOURCE_DIR = r"c:\MyResumePortfolio\images\blog\2026-01-28"
TARGET_WIDTH = 1200
QUALITY = 80

def optimize_images():
    print(f"Optimizing images in {SOURCE_DIR}...")
    
    total_savings = 0
    
    for filename in os.listdir(SOURCE_DIR):
        if filename.lower().endswith(".png"):
            filepath = os.path.join(SOURCE_DIR, filename)
            
            with Image.open(filepath) as img:
                # 1. Resize if needed
                if img.width > TARGET_WIDTH:
                    ratio = TARGET_WIDTH / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((TARGET_WIDTH, new_height), Image.Resampling.LANCZOS)
                    print(f"Resized {filename} to {TARGET_WIDTH}px width.")

                # 2. Convert to WebP
                webp_filename = os.path.splitext(filename)[0] + ".webp"
                webp_path = os.path.join(SOURCE_DIR, webp_filename)
                
                img.save(webp_path, "WEBP", quality=QUALITY)
                
                # Stats
                original_size = os.path.getsize(filepath)
                new_size = os.path.getsize(webp_path)
                savings = original_size - new_size
                total_savings += savings
                
                print(f"Converted {filename}: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB ({savings/original_size*100:.1f}% savings)")

    print(f"\nTotal Space Saved: {total_savings/1024:.1f}KB")

if __name__ == "__main__":
    optimize_images()
