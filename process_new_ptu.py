import os
from PIL import Image

# Configuration
SOURCE_FILE = r"C:\MyResumePortfolio\uklifelabsaisolution\images\newptu.png"
TARGET_FILE = r"c:\MyResumePortfolio\images\blog\2026-01-28\newptu.webp"
TARGET_WIDTH = 1200
QUALITY = 85

def process_new_ptu():
    print(f"Processing {SOURCE_FILE}...")
    
    if not os.path.exists(SOURCE_FILE):
        print(f"Error: Source file not found: {SOURCE_FILE}")
        return

    try:
        with Image.open(SOURCE_FILE) as img:
            # 1. Resize if needed
            if img.width > TARGET_WIDTH:
                ratio = TARGET_WIDTH / img.width
                new_height = int(img.height * ratio)
                img = img.resize((TARGET_WIDTH, new_height), Image.Resampling.LANCZOS)
                print(f"Resized from {img.width} to {TARGET_WIDTH}px width.")

            # 2. Convert to WebP
            img.save(TARGET_FILE, "WEBP", quality=QUALITY)
            
            # Stats
            original_size = os.path.getsize(SOURCE_FILE)
            new_size = os.path.getsize(TARGET_FILE)
            savings = original_size - new_size
            
            print(f"Success! Saved to {TARGET_FILE}")
            print(f"Size: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB ({savings/original_size*100:.1f}% savings)")
            
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    process_new_ptu()
