import os
from PIL import Image

# Configuration
TARGET_WIDTH = 1024
TARGET_HEIGHT = 576
# No background color needed for crop
IMG_DIR = r"C:\MyResumePortfolio\images\blog\2026-01-15"

# Map generated files to target filenames
FILE_MAPPINGS = {
    "azure_migrate_architecture_v2_dark_1768470847285.png": "azure-migrate-architecture.png",
    "tco_comparison_chart_v2_dark_1768470871084.png": "tco-comparison-chart.png",
    "business_case_dashboard_v2_dark_1768470894133.png": "business-case-dashboard.png",
    "dependency_map_network_v2_dark_1768470914982.png": "dependency-map.png"
}

GEN_DIR = r"C:\Users\upend\.gemini\antigravity\brain\2a0f9f26-073c-4484-95f7-8e0714e237a6"

def process_images_crop():
    if not os.path.exists(IMG_DIR):
        print(f"Directory not found: {IMG_DIR}")
        return

    for gen_file, target_name in FILE_MAPPINGS.items():
        source_path = os.path.join(GEN_DIR, gen_file)
        target_path = os.path.join(IMG_DIR, target_name)
        
        if not os.path.exists(source_path):
            print(f"Source not found: {gen_file}")
            continue

        try:
            with Image.open(source_path) as img:
                print(f"Processing {target_name} from {gen_file}...")
                
                # Center Crop Logic
                # Original is 1024x1024. We want 1024x576.
                # Since widths match, we just crop height.
                
                left = 0
                right = img.width
                
                # Calculate vertical center
                top = (img.height - TARGET_HEIGHT) / 2
                bottom = (img.height + TARGET_HEIGHT) / 2
                
                cropped_img = img.crop((left, top, right, bottom))
                
                # Save to target
                cropped_img.save(target_path)
                print(f"Done: {target_name} (Cropped to {TARGET_WIDTH}x{TARGET_HEIGHT})")
                
        except Exception as e:
            print(f"Error processing {target_name}: {e}")

if __name__ == "__main__":
    process_images_crop()
