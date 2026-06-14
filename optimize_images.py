import os
from PIL import Image

# Configuration
SOURCE_DIR = r"c:\MyResumePortfolio\blog\assets\2026-01-26-dns-pattern"
MAX_WIDTH = 1200
QUALITY = 80

def optimize_images():
    print(f"Scanning {SOURCE_DIR}...")
    
    files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith('.png')]
    
    for filename in files:
        filepath = os.path.join(SOURCE_DIR, filename)
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
        
        # Only process if > 500KB (arbitrary threshold, but good for "large" check)
        # Actually, let's process all PNGs in this specific folder to be consistent with WebP
        
        print(f"Processing {filename} ({file_size_mb:.2f} MB)...")
        
        try:
            with Image.open(filepath) as img:
                # Convert to RGB (in case of RGBA) for safety if saving as non-supporting format, 
                # but WebP supports transparency, so we keep RGBA if present.
                
                # Resize if needed
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                    print(f"  Resized to {MAX_WIDTH}x{new_height}")
                
                # Save as WebP
                webp_filename = os.path.splitext(filename)[0] + ".webp"
                webp_path = os.path.join(SOURCE_DIR, webp_filename)
                
                img.save(webp_path, "WEBP", quality=QUALITY)
                
                new_size_mb = os.path.getsize(webp_path) / (1024 * 1024)
                print(f"  Saved as {webp_filename} ({new_size_mb:.2f} MB)")
                print(f"  Reduction: {(1 - new_size_mb/file_size_mb)*100:.1f}%")
                
        except Exception as e:
            print(f"  Error processing {filename}: {e}")

if __name__ == "__main__":
    optimize_images()
