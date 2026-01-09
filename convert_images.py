import os
from PIL import Image

directory = r'c:\MyResumePortfolio\images\blog'

for filename in os.listdir(directory):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and not filename.lower().endswith('.webp'):
        filepath = os.path.join(directory, filename)
        new_filepath = os.path.splitext(filepath)[0] + '.webp'
        
        try:
            with Image.open(filepath) as img:
                img.save(new_filepath, 'webp')
                print(f"Converted {filename} to {os.path.basename(new_filepath)}")
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
