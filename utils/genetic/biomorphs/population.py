import math
import random
from PIL import Image, ImageDraw


class Biomorph:
    def __init__(self):
        self.body = None
        self.head = None
        self.legs = []


def generate_default_body(start_x, start_y, biomorph, img_size, color):
    # Fill this
    if start_x is None or start_y is None:
        # Use default center coordinates if the body was not provided
        start_x, start_y = img_size[0] / 2, img_size[1] / 2

    foot_radius = 50
    biomorph.body = ({'type': 'ellipse',
                      'x1': start_x - foot_radius,
                      'y1': start_y - foot_radius,
                      'width': foot_radius * 2,
                      'height': foot_radius * 2,
                      'color': color})
    return biomorph.body


def generate_leg(start_x=None, start_y=None, color=None, width=1):
    length = 10
    angle = random.random() * 0.5 * math.pi  # Random angle (0 to 90 degrees)
    end_x = int(start_x + length * math.cos(angle))
    end_y = int(start_y + length * math.sin(angle))
    leg = ({'type': 'line',
            'x1': start_x, 'y1': start_y,
            'x2': end_x, 'y2': end_y,
            'width': width,
            'color': color})

    return leg


def generate_biomorph(start_x=None, start_y=None, legs_amount=4, img_size=(300, 300), biomorph=None):
    if biomorph is None:
        biomorph = Biomorph()
        color = random.choice(['red', 'green', 'blue'])
        width = random.randint(3, 5)
    else:
        color = biomorph.legs[0]['color']
        width = biomorph.legs[0]['width']

    if start_x is None or start_y is None:
        # Start at the center if no start coordinates were given
        start_x, start_y = img_size[0] / 2, img_size[1] / 2

    if biomorph.body is None:
        biomorph.body = generate_default_body(start_x, start_y, biomorph, img_size, color)

    if not biomorph.legs:
        biomorph.legs.append(generate_leg(start_x, start_y, color, width))

    while legs_amount > 0:
        # Option to create the next segment starting from a random previously generated segment
        #                      last_part = biomorph.legs[random.randint(-len(biomorph.legs), -1)]
        last_part = biomorph.legs[-1]
        new_start_x = last_part['x2']
        new_start_y = last_part['y2']
        biomorph.legs.append(generate_leg(new_start_x, new_start_y, color, width))
        legs_amount = legs_amount - 1
    else:
        # Generate foot
        foot_radius = 5
        last_x, last_y = biomorph.legs[-1]['x2'], biomorph.legs[-1]['y2']
        biomorph.legs.append({
            'type': 'ellipse',
            'x1': last_x - foot_radius,
            'y1': last_y - foot_radius,
            'width': foot_radius * 2,
            'height': foot_radius * 2,
            'color': color
        })
    return biomorph


def draw_biomorph(biomorph, img_size=(300, 300)):
    img = Image.new('RGB', img_size, color='white')
    draw = ImageDraw.Draw(img)

    xy = (biomorph.body['x1'], biomorph.body['y1'], biomorph.body['x1'] + biomorph.body['width'],
          biomorph.body['y1'] + biomorph.body['height'])
    draw.ellipse(xy, fill=biomorph.body['color'])

    for part in biomorph.legs:
        if part['type'] == 'line':
            draw.line((part['x1'], part['y1'], part['x2'], part['y2']),
                      fill=part['color'], width=part['width'])
        if part['type'] == 'ellipse':
            xy = (part['x1'], part['y1'], part['x1'] + part['width'],
                  part['y1'] + part['height'])
            draw.ellipse(xy, fill=part['color'])

    return img


# Example usage (For now, let's print the Biomorph structure)
my_biomorph = generate_biomorph(legs_amount=10)
draw_biomorph(my_biomorph).show()
