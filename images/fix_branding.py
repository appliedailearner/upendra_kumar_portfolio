from PIL import Image, ImageDraw, ImageFont
import os

def fix_branding():
    img_path = 'c:/MyResumePortfolio/images/azure_resilience_infographic.png'
    output_path = 'c:/MyResumePortfolio/images/azure_resilience_infographic.png'
    
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found.")
        return

    img = Image.open(img_path)
    # Ensure it's in RGB mode
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # We identified the watermark in the bottom right corner (last 500x100px)
    # Background color is White (255, 255, 255)
    
    # Define a generous area to clear (bottom right corner)
    # NotebookLM and Logo are roughly in the bottom 400px of width and 100px of height
    rect_x0 = width - 450
    rect_y0 = height - 120
    rect_x1 = width
    rect_y1 = height
    
    # Clear the old branding with a clean white box
    draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=(255, 255, 255))
    
    # Add the custom portfolio URL
    text = "https://portfolio.upendrakumar.com/"
    
    # Try to use a professional font (Arial is common on Windows)
    try:
        # 1536 height image. 28px font is professional/small
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()
    
    # Draw the text in a professional gray color consistent with infographic footers
    text_color = (60, 60, 60) # Dark gray
    
    # Position the text with some padding from the right and bottom
    text_x = width - 480
    text_y = height - 60
    
    draw.text((text_x, text_y), text, fill=text_color, font=font)
    
    # Save the result
    img.save(output_path, quality=95)
    print(f"Successfully updated branding to: {text}")

if __name__ == "__main__":
    fix_branding()
