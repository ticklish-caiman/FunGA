import math
import random


class Biomorph:
    def __init__(self):
        self.body = None
        self.head = None
        self.left_eye = None
        self.right_eye = None
        self.legs = []


def generate_default_body(body_radius, start_x, start_y, biomorph, img_size, color):
    # Fill this
    if start_x is None or start_y is None:
        # Use default center coordinates if the body was not provided
        start_x, start_y = img_size[0] / 2, img_size[1] / 2

    biomorph.body = ({'type': 'ellipse',
                      'x1': start_x - body_radius,
                      'y1': start_y - body_radius,
                      'width': body_radius * 2,
                      'height': body_radius * 2,
                      'color': color})
    return biomorph.body


def generate_leg(start_x=None, start_y=None, color=None, width=1, angle=0):
    length = 30
    end_x = int(start_x + length * math.cos(angle))
    end_y = int(start_y + length * math.sin(angle))
    leg = ({'type': 'line',
            'x1': start_x, 'y1': start_y,
            'x2': end_x, 'y2': end_y,
            'width': width,
            'color': color})

    return leg


def generate_legs(biomorph, start_x, start_y, num_legs, color, width, angle):
    if num_legs == 0:
        # Generate foot
        foot_radius = 10
        last_x, last_y = biomorph.legs[-1]['x2'], biomorph.legs[-1]['y2']
        biomorph.legs.append({
            'type': 'ellipse',
            'x1': last_x - foot_radius,
            'y1': last_y - foot_radius,
            'width': foot_radius * 2,
            'height': foot_radius * 2,
            'color': color
        })
        return

    biomorph.legs.append(generate_leg(start_x, start_y, color, width, angle))
    last_part = biomorph.legs[-1]

    generate_legs(biomorph, last_part['x2'], last_part['y2'], num_legs - 1, color, width, angle)


def generate_head(head_radius, body, color):
    head_x = body['x1'] + (body['width'] / 2)  # Center of the head above body's center
    head_y = body['y1'] - head_radius  # Place head's bottom edge on top of the body

    # Eye calculations
    eye_radius = head_radius * 0.1  # Example: Eye radius is 10% of the head radius
    eye_offset_x = head_radius * 0.3  # Eyes offset horizontally by 30% of head radius
    eye_offset_y = head_radius * 0.3  # Eyes raised slightly from the center

    # Eyes (two circles)
    left_eye = {
        'type': 'circle',
        'x1': head_x - eye_offset_x,
        'y1': head_y + eye_offset_y,
        'radius': eye_radius,
        'color': 'black'
    }
    right_eye = {
        'type': 'circle',
        'x1': head_x + eye_offset_x,
        'y1': head_y + eye_offset_y,
        'radius': eye_radius,
        'color': 'black'
    }

    head = {'type': 'ellipse',
            'x1': head_x - head_radius,
            'y1': head_y - head_radius,
            'width': head_radius * 2,
            'height': head_radius * 2,
            'color': color}

    return head, left_eye, right_eye


def generate_biomorph(genes, start_x=None, start_y=None, img_size=(500, 500), biomorph=None):
    if biomorph is None:
        biomorph = Biomorph()

    if start_x is None or start_y is None:
        # Start at the center if no start coordinates were given
        start_x, start_y = img_size[0] / 2, img_size[1] / 2

    if biomorph.body is None:
        biomorph.body = generate_default_body(genes['body_radius'], start_x, start_y, biomorph, img_size,
                                              genes['color'])

    if biomorph.head is None:
        biomorph.head, biomorph.left_eye, biomorph.right_eye = generate_head(genes['head_radius'], biomorph.body,
                                                                             genes['color'])

    for angle in range(genes['leg_count']):
        generate_legs(biomorph, start_x, start_y, genes['leg_segments'], genes['color'], genes['leg_width'], angle)

    return biomorph
