import random
from PIL import Image, ImageDraw


class Biomorph:
    def __init__(self):
        self.parts = []


def generate_random_biomorph(start_x=None, start_y=None, shapes_amount=5, img_size=(300, 300), biomorph=None):
    if biomorph is None:
        new_biomorph = Biomorph()
    else:
        new_biomorph = biomorph
    if start_x is None or start_y is None:
        start_x, start_y = img_size[0] / 2, img_size[1] / 2

    # Create the initial line
    end_x = start_x + random.randint(-50, 50)
    end_y = start_y + random.randint(-50, 50)
    new_biomorph.parts.append({'type': 'line',
                               'x1': start_x, 'y1': start_y,
                               'x2': end_x, 'y2': end_y,
                               'width': random.randint(3, 5),  # Line width
                               'color': random.choice(['red', 'green', 'blue'])})
    print('after append:', new_biomorph.parts)
    print('start_x:', start_x, 'start_y:', start_y, 'end_x:', end_x, 'end_y:', end_y)
    if shapes_amount > 0:
        last_part = new_biomorph.parts[-1]
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
my_biomorph = generate_random_biomorph()
draw_biomorph(my_biomorph).show()
