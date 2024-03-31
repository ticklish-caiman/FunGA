import math

from PIL import Image, ImageDraw


def draw_image_from_array(binary_array):
    width = len(binary_array[0])  # Get width from the first row
    height = len(binary_array)  # Get height from the number of rows

    image = Image.new('RGB', (width, height), color='white')  # Create a white image
    draw = ImageDraw.Draw(image)

    # Iterate over the array, drawing pixels
    for y, row in enumerate(binary_array):
        for x, pixel in enumerate(row):
            if pixel == 1:
                draw.point((x, y), fill='black')  # Draw a black pixel

    return image


def draw_tree(image, draw, x, y, length, angle):
    if length < 5:  # Stop drawing if branches get too small
        return

    x2 = x + int(math.cos(angle) * length)
    y2 = y + int(math.sin(angle) * length)

    draw.line((x, y, x2, y2), fill='brown', width=2)  # Draw branch

    draw_tree(image, draw, x2, y2, length * 0.8, angle - 0.2)  # Recursion left
    draw_tree(image, draw, x2, y2, length * 0.8, angle + 0.2)  # Recursion right


image = Image.new('RGB', (200, 200), color='white')
draw = ImageDraw.Draw(image)
draw_tree(image, draw, 100, 180, 60, -math.pi / 2)  # Start at the bottom
