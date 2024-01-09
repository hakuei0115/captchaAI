from PIL import Image, ImageDraw, ImageFont
import random

def get_rand_color(min_val, max_val):
    """ Generate a random color """
    return (random.randint(min_val, max_val), random.randint(min_val, max_val), random.randint(min_val, max_val))

def get_captcha_with_corrected_text_sizing(width, height):
    """ Generate a captcha image with 6 random characters centered, correcting text sizing """
    # Define the character set
    char_set = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Generate a random string of 6 characters
    random_str = ''.join(random.choices(char_set, k=6))

    # Create a new image with white background
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Fill background with random color
    draw.rectangle([(0, 0), (width, height)], fill=get_rand_color(200, 250))

    # Set a uniform color for interference lines
    line_color = get_rand_color(160, 200)

    # Draw random interference lines with uniform color
    for _ in range(155):
        start = (random.randint(0, width), random.randint(0, height))
        end = (start[0] + random.randint(0, 12), start[1] + random.randint(0, 12))
        draw.line([start, end], fill=line_color, width=1)

    # Draw characters with fixed spacing
    font = ImageFont.load_default()  # Default font
    char_spacing = width // 6
    for i, char in enumerate(random_str):
        bbox = draw.textbbox((0, 0), char, font=font)
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]
        x = char_spacing * i + (char_spacing - char_width) // 2
        y = (height - char_height) // 2
        draw.text((x, y), char, font=font, fill=get_rand_color(20, 130))

    return image, random_str

# Example usage
captcha_image_corrected, captcha_str = get_captcha_with_corrected_text_sizing(120, 50)
captcha_image_corrected.show()  # This will open the image in the default image viewer

# To display the image in this notebook environment, we convert it to a format compatible with Jupyter
captcha_image_corrected.save("captcha_corrected_text_sizing.png")