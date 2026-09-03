import sys
from PIL import Image, ImageDraw, ImageFont

# Define paths
bg_color = (15, 23, 42) # slate-900
w, h = 1200, 630
img_out_path = r"C:\MyResumePortfolio\images\blog\forced_tunneling_social.webp"
diagram_path = r"C:\MyResumePortfolio\images\blog\core_routing_pro.webp"

# Create base canvas
img = Image.new('RGB', (w, h), color=bg_color)
draw = ImageDraw.Draw(img)

# Try to load the architecture diagram and paste it on the right side
try:
    diag = Image.open(diagram_path)
    # Resize diagram to fit nicely if needed
    diag.thumbnail((600, 500), Image.Resampling.LANCZOS)
    x_offset = w - diag.width - 50
    y_offset = (h - diag.height) // 2
    
    # We create a white rounded rectangle background for the diagram so it pops
    draw.rounded_rectangle([x_offset - 20, y_offset - 20, x_offset + diag.width + 20, y_offset + diag.height + 20], radius=15, fill=(255,255,255))
    
    # Paste diagram
    img.paste(diag, (x_offset, y_offset), diag if diag.mode == 'RGBA' else None)
except Exception as e:
    print(f"Diagram error: {e}")

# Add text on the left side
try:
    font_title = ImageFont.truetype("arialbd.ttf", 60)
    font_subtitle = ImageFont.truetype("arial.ttf", 35)
except:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()

title = "Breaking the Cloud:\nAzure Forced\nTunneling"
subtitle = "The Survival Guide to\nResolving Asymmetric\nRouting & KMS Failures."

draw.text((60, 180), title, font=font_title, fill=(255, 255, 255))
draw.text((60, 400), subtitle, font=font_subtitle, fill=(56, 189, 248)) # sky-400

# Save out
img.save(img_out_path, "WEBP", quality=95)
print("Saved social card to:", img_out_path)
