from PIL import ImageDraw, Image


def draw_circle(image, center_x, center_y, radius, color=0):
    draw = ImageDraw.Draw(image)
    bbox = (center_x - radius, center_y - radius, center_x + radius, center_y + radius)
    draw.ellipse(bbox, fill=color)


def draw_rectangle(image, center_x, center_y, width, height, color=0):
    draw = ImageDraw.Draw(image)
    bbox = [(center_x - width // 2, center_y - height // 2),
            (center_x + width // 2, center_y + height // 2)]
    draw.rectangle(bbox, fill=color)


def generate_image(genome):
    image = Image.new("L", (500, 500), color=255)  # White (255) background, "L" mode for grayscale

    for shape_params in genome:
        if shape_params['type'] == 'circle':
            draw_circle(image,
                        shape_params['center_x'], shape_params['center_y'],
                        shape_params['radius'])
        elif shape_params['type'] == 'rectangle':
            draw_rectangle(image,
                           shape_params['center_x'], shape_params['center_y'],
                           shape_params['width'], shape_params['height'])

    return image
