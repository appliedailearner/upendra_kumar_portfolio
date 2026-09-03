import os
from PIL import Image

dir_path = r"C:\MyResumePortfolio\images\blog"
# also converting the generated ones in the artifacts dir just in case
artifacts_path = r"C:\Users\upend\.gemini\antigravity\brain\f8cf40ca-8d39-4eae-a103-d569d17b22d2"

def convert_dir(d):
    count = 0
    if os.path.exists(d):
        for file in os.listdir(d):
            if file.endswith("_pro.png"):
                img_path = os.path.join(d, file)
                webp_path = os.path.join(d, file.replace(".png", ".webp"))
                try:
                    img = Image.open(img_path)
                    img.save(webp_path, "WEBP", quality=90)
                    print(f"Converted: {file} -> {os.path.basename(webp_path)}")
                    count += 1
                except Exception as e:
                    print(f"Error on {file}: {e}")
    return count

print("Converting blog directory...")
c1 = convert_dir(dir_path)
print("Converting artifacts directory...")
c2 = convert_dir(artifacts_path)
print(f"Total converted: {c1+c2}")
