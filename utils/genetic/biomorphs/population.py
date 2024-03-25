import math
import random
from PIL import Image, ImageDraw


class Biomorph:
    def __init__(self):
        self.parts = []


def generate_random_biomorph(start_x=None, start_y=None, shapes_amount=5, img_size=(300, 300), new_biomorph=None):
    if new_biomorph is None:
        new_biomorph = Biomorph()
        color = random.choice(['red', 'green', 'blue'])
        width = random.randint(3, 5)
    else:
        color = new_biomorph.parts[0]['color']
        width = new_biomorph.parts[0]['width']

    if start_x is None or start_y is None:
        # Start at the center if no start coordinates were given
        start_x, start_y = img_size[0] / 2, img_size[1] / 2

    # Create the initial line
    length = 50  # Calculate the desired length
    angle = random.random() * 1 * math.pi  # Random angle (0 to 180 degrees)
    end_x = int(start_x + length * math.cos(angle))
    end_y = int(start_y + length * math.sin(angle))
    new_biomorph.parts.append({'type': 'line',
                               'x1': start_x, 'y1': start_y,
                               'x2': end_x, 'y2': end_y,
                               'width': width,
                               'color': color})
    print('after append:', new_biomorph.parts)
    print('start_x:', start_x, 'start_y:', start_y, 'end_x:', end_x, 'end_y:', end_y)
    if shapes_amount > 0:
        last_part = new_biomorph.parts[random.randint(-len(new_biomorph.parts), -1)]
        # last_part = new_biomorph.parts[-1]
        new_start_x = last_part['x2']
        new_start_y = last_part['y2']
        print('new_start_x:', new_start_x, 'new_start_y:', new_start_y)
        generate_random_biomorph(new_start_x, new_start_y, shapes_amount - 1, img_size, new_biomorph)

    return new_biomorph


def draw_biomorph(biomorph, img_size=(300, 300)):
    img = Image.new('RGB', img_size, color='white')
    draw = ImageDraw.Draw(img)

    for part in biomorph.parts:
        if part['type'] == 'line':
            draw.line((part['x1'], part['y1'], part['x2'], part['y2']),
                      fill=part['color'], width=part['width'])

        elif part['type'] == 'ellipse':
            xy = (part['x1'], part['y1'], part['x1'] + part['width'], part['y1'] + part['height'])
            draw.ellipse(xy, fill=part['color'])

        elif part['type'] == 'rectangle':
            # TODO: Implement rectangle drawing using xy coordinates and width/height
            pass

    return img


# Example usage (For now, let's print the Biomorph structure)
my_biomorph = generate_random_biomorph(shapes_amount=10)
draw_biomorph(my_biomorph).show()
