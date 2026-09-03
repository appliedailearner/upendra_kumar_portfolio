import os
from PIL import Image

images_dir = r"C:\MyResumePortfolio\images"
blog_images = [
    "hero_chaos.png",
    "agent_mediation_layer.jpg",
    "ai-landing-zone-vnet.png",
    "four_pillars_of_proof.png"
]

for filename in blog_images:
    file_path = os.path.join(images_dir, filename)
    if os.path.exists(file_path):
        try:
            img = Image.open(file_path)
            # Ensure RGBA for png, RGB for jpeg
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA') if img.info.get('transparency') else img.convert('RGB')
            
            webp_path = os.path.join(images_dir, os.path.splitext(filename)[0] + '.webp')
            img.save(webp_path, 'webp', quality=85)
            print(f"Converted {filename} -> {os.path.basename(webp_path)}")
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
    else:
        print(f"File not found: {file_path}")
