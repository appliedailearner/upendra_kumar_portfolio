import os
from PIL import Image

def optimize_images(root_dir, max_width=1600, quality=85):
    supported_formats = ('.png', '.jpg', '.jpeg')
    stats = {
        'count': 0,
        'original_size': 0,
        'webp_size': 0
    }

    print(f"Starting optimization in {root_dir}...")

    for subdir, _, files in os.walk(root_dir):
        # Skip directories like .git or node_modules if they exist inside root_dir
        if any(ignored in subdir for ignored in ['.git', 'node_modules', '.terraform']):
            continue

        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(subdir, file)
                webp_path = os.path.splitext(file_path)[0] + '.webp'

                try:
                    with Image.open(file_path) as img:
                        original_size = os.path.getsize(file_path)
                        
                        # Convert to RGB if necessary (e.g., for PNG with transparency or CMYK)
                        # WebP supports transparency, so we don't necessarily need to convert to RGB 
                        # but some modes might need conversion.
                        
                        # Resize if larger than max_width
                        if img.width > max_width:
                            w_percent = (max_width / float(img.width))
                            h_size = int((float(img.height) * float(w_percent)))
                            img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
                        
                        # Save as WebP
                        img.save(webp_path, 'WEBP', quality=quality, lossless=False)
                        
                        webp_size = os.path.getsize(webp_path)
                        
                        stats['count'] += 1
                        stats['original_size'] += original_size
                        stats['webp_size'] += webp_size
                        
                        print(f"Optimized: {file} -> {os.path.basename(webp_path)} ({webp_size/1024:.1f} KB)")
                except Exception as e:
                    print(f"Failed to process {file}: {e}")

    if stats['count'] > 0:
        savings = (1 - (stats['webp_size'] / stats['original_size'])) * 100
        print("\nOptimization Summary:")
        print(f"Total Images Optimized: {stats['count']}")
        print(f"Original Total Size: {stats['original_size']/1024/1024:.2f} MB")
        print(f"WebP Total Size: {stats['webp_size']/1024/1024:.2f} MB")
        print(f"Total Savings: {savings:.1f}%")
    else:
        print("No images found to optimize.")

if __name__ == "__main__":
    # Get project root (parent of scripts/)
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # We'll scan specific high-value folders first, or the whole root excluding code folders
    target_folders = [
        os.path.join(project_root, 'images'),
        os.path.join(project_root, 'blog')
    ]
    
    for folder in target_folders:
        if os.path.exists(folder):
            optimize_images(folder)
