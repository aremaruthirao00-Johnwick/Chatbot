from PIL import Image, ImageDraw, ImageFont
import os

def create_avatar(text, filename, bg_color, text_color="white"):
    size = (100, 100)
    img = Image.new('RGBA', size, (0, 0, 0, 0)) # Transparent background
    draw = ImageDraw.Draw(img)
    
    # Draw circle
    draw.ellipse([0, 0, 100, 100], fill=bg_color)
    
    # Draw text
    try:
        # Try to load a nice font, otherwise default
        font = ImageFont.truetype("Arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Center text (rough estimation for default font, better methods exist but this suffices)
    # Using textbbox if available (Pillow >= 8.0.0)
    try:
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        w = right - left
        h = bottom - top
    except:
        w, h = draw.textsize(text, font=font)
        
    draw.text(((100-w)/2, (100-h)/2), text, fill=text_color, font=font)
    
    img.save(filename)
    print(f"Created {filename}")

if __name__ == "__main__":
    output_dir = "chatbot_app"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Create ME icon (Blueish to match user theme)
    create_avatar("ME", os.path.join(output_dir, "me_icon.png"), "#1a73e8")
    
    # Create AI icon (Greenish to match AI theme)
    create_avatar("AI", os.path.join(output_dir, "ai_icon.png"), "#34a853")
