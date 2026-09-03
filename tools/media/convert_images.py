import urllib.request
from PIL import Image
import os

images_to_convert = {
    "https://learn.microsoft.com/en-us/azure/databricks/_static/images/security/network/pl-azure-fe.png": "pl-azure-fe.webp",
    "https://learn.microsoft.com/en-us/azure/databricks/_static/images/security/network/pl-azure-be.png": "pl-azure-be.webp"
}

output_dir = "assets/images"
os.makedirs(output_dir, exist_ok=True)

for url, filename in images_to_convert.items():
    print(f"Downloading {url}...")
    try:
        temp_file = "temp_image.png"
        urllib.request.urlretrieve(url, temp_file)
        print(f"Converting {temp_file} to {filename}...")
        img = Image.open(temp_file)
        img.save(os.path.join(output_dir, filename), "WEBP")
        os.remove(temp_file)
        print(f"Successfully created {filename}")
    except Exception as e:
        print(f"Error processing {url}: {e}")
