import os
from PIL import Image

def convert_to_webp(directory):
    print(f"Scanning {directory}...")
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            filepath = os.path.join(directory, filename)
            webp_filename = os.path.splitext(filename)[0] + ".webp"
            webp_filepath = os.path.join(directory, webp_filename)
            
            try:
                with Image.open(filepath) as img:
                    print(f"Converting {filename} to WebP...")
                    img.save(webp_filepath, "WEBP", quality=80)
                    
                    original_size = os.path.getsize(filepath)
                    new_size = os.path.getsize(webp_filepath)
                    savings = (original_size - new_size) / original_size * 100
                    
                    print(f"Saved {webp_filename} ({new_size/1024:.2f} KB). Reduced by {savings:.1f}%")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

if __name__ == "__main__":
    projects_dir = os.path.join("portfolio-deploy", "assets", "images", "projects")
    if os.path.exists(projects_dir):
        convert_to_webp(projects_dir)
    else:
        print(f"Directory not found: {projects_dir}")
