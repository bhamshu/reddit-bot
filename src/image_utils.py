from PIL import Image, ImageDraw, ImageFont
import textwrap

def generate_image_with_text(text, image_size=(1024, 1024), font_path='arial.ttf', font_size=40, line_spacing=10):
    # Load or create the background image
    image = Image.new('RGB', image_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Load a font
    # font = ImageFont.truetype(font_path, font_size)
    font = ImageFont.load_default()

    
    # Calculate text size and position
    char_width, char_height = font.getsize('A')  # Approximation of character size
    max_chars_per_line = image_size[0] // char_width
    wrapped_text = textwrap.fill(text, width=max_chars_per_line)
    
    # Calculate text height for vertical centering
    lines = wrapped_text.split('\n')
    text_height = char_height * len(lines) + line_spacing * (len(lines) - 1)
    
    # Calculate starting Y position
    start_y = (image_size[1] - text_height) // 2
    
    # Draw text on image
    y = start_y
    for line in lines:
        text_width, text_height = draw.textsize(line, font=font)
        x = (image_size[0] - text_width) // 2
        draw.text((x, y), line, font=font, fill=(0, 0, 0))
        y += char_height + line_spacing
    
    return image
# Example usage
text_input = "This is an example of a beautifully formatted text, generated to fit nicely within an image. The script ensures the text is centered and wrapped appropriately."
image_path = generate_image_with_text(text_input)
print(f"Image successfully generated at {image_path}")
