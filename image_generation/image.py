from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_decorated_image(title, text, quote, bg_color, text_color, filename='decorated_image.png'):
    # Convert hex color codes to RGB tuples
    bg_rgb = hex_to_rgb(bg_color)
    text_rgb = hex_to_rgb(text_color)

    # Initialize the dimensions and padding for the image
    img_width, img_height = 800, 800
    vertical_padding = 40  # Top and bottom padding
    space_between_title_and_text = 30
    space_between_text_and_quote = 30
    x_padding = 10  # Horizontal padding for title and quote

    # Create an image with the specified background color
    img = Image.new('RGB', (img_width, img_height), color=bg_rgb)
    draw = ImageDraw.Draw(img)

    # Define font paths and load fonts
    font_paths = {
        "title": "image_generation/fonts/uni-sans/Uni-Sans-Heavy.otf",
        "text": "image_generation/fonts/poppins/Poppins-Regular.ttf",
        "quote": "image_generation/fonts/poppins/Poppins-BoldItalic.ttf"
    }
    try:
        title_font = ImageFont.truetype(font_paths["title"], 64)
        text_font = ImageFont.truetype(font_paths["text"], 32)
        quote_font = ImageFont.truetype(font_paths["quote"], 48)
    except Exception as e:
        print(f"An error occurred while loading the fonts: {e}")
        title_font = text_font = quote_font = ImageFont.load_default()

    # Measure and layout text
    wrapped_title = textwrap.wrap(title, width=20)
    wrapped_text = textwrap.wrap(text, width=45)
    wrapped_quote = textwrap.wrap(quote, width=25)

    # Measure total content height
    total_content_height = vertical_padding
    line_spacing = 5
    underline_thickness = 2
    underline_gap = 5
    for line in wrapped_title + wrapped_text + wrapped_quote:
        _, line_height = draw.textbbox((0, 0), line, font=title_font if line in wrapped_title else text_font if line in wrapped_text else quote_font)[2:]
        total_content_height += line_height + line_spacing + (underline_gap + underline_thickness if line in wrapped_title else 0)
    total_content_height += space_between_title_and_text + space_between_text_and_quote - line_spacing

    # Calculate starting Y position
    current_y = (img_height - total_content_height) / 2

    # Draw title with x-padding
    for line in wrapped_title:
        line_width, line_height = draw.textbbox((0, 0), line, font=title_font)[2:]
        line_x = x_padding + (img_width - 2 * x_padding - line_width) / 2
        draw.text((line_x, current_y), line, font=title_font, fill=text_rgb)
        draw.line([(line_x, current_y + line_height + underline_gap), 
                   (line_x + line_width, current_y + line_height + underline_gap)],
                  fill=text_rgb, width=underline_thickness)
        current_y += line_height + line_spacing + underline_gap + underline_thickness
    current_y += space_between_title_and_text - line_spacing

    # Draw text without x-padding
    for line in wrapped_text:
        line_width, line_height = draw.textbbox((0, 0), line, font=text_font)[2:]
        line_x = (img_width - line_width) / 2
        draw.text((line_x, current_y), line, font=text_font, fill=text_rgb)
        current_y += line_height + line_spacing

    current_y += space_between_text_and_quote - line_spacing

    # Draw quote with x-padding
    for line in wrapped_quote:
        line_width, line_height = draw.textbbox((0, 0), line, font=quote_font)[2:]
        line_x = x_padding + (img_width - 2 * x_padding - line_width) / 2
        draw.text((line_x, current_y), line, font=quote_font, fill=text_rgb)
        current_y += line_height + line_spacing

    # Save the image
    img.save(filename)
    print(f"Image saved as {filename}")

    return filename

# Function to convert hex color code to RGB tuple
def hex_to_rgb(hex_code):
    # Remove '#' if present and convert hex code to RGB
    hex_code = hex_code.lstrip('#')
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return rgb

# Example text to include in the image
text = "Personal growth often involves respecting our own boundaries. It seems like honesty and open communication are crucial in this situation, even if it involves difficult conversations. Finding a middle ground that respects both your partner's wishes and your comfort is essential."

# Example usage with specified background and text colors
bg_color = '#F0EAD6'   # Light Blue
text_color = '#635F6D'  # Black
create_decorated_image(title="Navigating Name Dilemma",text=text, bg_color=bg_color, text_color=text_color, quote="Honesty is the cornerstone of authentic relationships.")
