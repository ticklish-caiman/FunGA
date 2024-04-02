import logging
import random

logging.basicConfig(level=logging.INFO)


def generate_genome(image_width, image_height, max_num_shapes=5):
    genome = []
    num_shapes = random.randint(1, max_num_shapes)
    for _ in range(num_shapes):
        shape_type = random.choice(['circle', 'rectangle'])
        center_x = random.randint(0, image_width - 1)
        center_y = random.randint(0, image_height - 1)

        if shape_type == 'circle':
            # Ensure radius fits within image bounds
            max_radius = min(center_x, center_y, image_width - center_x, image_height - center_y)
            logging.info('Max radius: {}'.format(max_radius))
            radius = random.randint(1, max_radius)
            shape_params = {'type': shape_type, 'center_x': center_x, 'center_y': center_y, 'radius': radius}
        else:
            width = random.randint(20, image_width // random.randint(3, 10))
            height = random.randint(20, image_height // random.randint(3, 10))
            shape_params = {'type': shape_type, 'center_x': center_x, 'center_y': center_y, 'width': width,
                            'height': height}

        genome.append(shape_params)

    return genome
