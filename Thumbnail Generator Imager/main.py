from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def add_text_to_image(text, image_path='Thumbnail_Stock.png'):
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Define the area where the text will be placed
    box_top_left = (75, 650)
    box_width = 620
    box_height = 105
    
    # Define the path to the DejaVuSans font file
    font_path = "../Utils/dejavu-sans.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file {font_path} not found.")
    
    def find_optimal_font_size(text, max_width, max_height, font_path):
        font_size = 1  
        font = ImageFont.truetype(font_path, font_size)
        
        while True:
            font = ImageFont.truetype(font_path, font_size)
            wrapped_text = textwrap.fill(text, width=int(max_width / font.getbbox("A")[2]))
            text_width, text_height = draw.multiline_textsize(wrapped_text, font=font)
            
            if text_width <= max_width and text_height <= max_height:
                font_size += 1
            else:
                font_size -= 1
                font = ImageFont.truetype(font_path, font_size)
                wrapped_text = textwrap.fill(text, width=int(max_width / font.getbbox("A")[2]))
                return font, wrapped_text

    # Find the optimal font size
    font, wrapped_text = find_optimal_font_size(text, box_width, box_height, font_path)
    
    # Calculate the position to center the text
    text_width, text_height = draw.multiline_textsize(wrapped_text, font=font)
    text_x = box_top_left[0] + (box_width - text_width) / 2
    text_y = box_top_left[1] + (box_height - text_height) / 2
    
    # Draw the centered text onto the image
    draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill="black")
    
    # Save the new image
    new_image_name = '_'.join(text.split()[:3]) + '.png'
    image.save(new_image_name)
    print(f"Image saved as {new_image_name}")

# Get input text from the user
input_text = input("Enter the text to add to the image: ")
add_text_to_image(input_text)
