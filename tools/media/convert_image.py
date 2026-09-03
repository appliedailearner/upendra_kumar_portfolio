
from PIL import Image
import os
import sys

# Define paths
input_path = r"C:\MyResumePortfolio\assets\diagrams\png\Architecting Production ready AI Systems.png"
output_path = r"C:\MyResumePortfolio\assets\diagrams\png\Architecting Production ready AI Systems.webp"

try:
    print(f"Opening: {input_path}")
    img = Image.open(input_path)
    
    print(f"Converting to WebP...")
    # Save as WebP with quality 80 (standard for web)
    img.save(output_path, "WEBP", quality=80)
    
    # Verify sizes
    original_size = os.path.getsize(input_path) / (1024 * 1024)
    new_size = os.path.getsize(output_path) / (1024 * 1024)
    
    print(f"Success! Converted.")
    print(f"Original: {original_size:.2f} MB")
    print(f"WebP: {new_size:.2f} MB")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
