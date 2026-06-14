from PIL import Image
import os

image_path = r"c:\MyResumePortfolio\images\blog\2026-01-09\azure-openai-apim-ref-arch.webp"
output_path = r"c:\MyResumePortfolio\images\blog\2026-01-09\azure-openai-apim-ref-arch.webp"

try:
    with Image.open(image_path) as img:
        print(f"Original size: {img.size}")
        if img.width > 800:
            # maintain aspect ratio
            width = 800
            height = int((width / img.width) * img.height)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            img.save(output_path, "WEBP", quality=85)
            print(f"Resized to: {img.size}")
            print("Image resized successfully.")
        else:
            print("Image is already small enough.")
except Exception as e:
    print(f"Error resizing image: {e}")
