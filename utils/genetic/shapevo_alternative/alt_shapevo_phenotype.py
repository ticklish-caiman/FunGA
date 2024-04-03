import numpy as np
from PIL import ImageDraw, Image
import cv2


def generate_image_opencv(genome, image_width, image_height):
    image = np.zeros((image_height, image_width), dtype=np.uint8)  # Black background
    color = (255, 255, 255)
    for shape_params in genome:
        if shape_params['type'] == 'circle':
            cv2.circle(image, (int(shape_params['center_x']), int(shape_params['center_y'])),
                       int(shape_params['radius']), color, thickness=-1)

        elif shape_params['type'] == 'rectangle':
            cv2.rectangle(image,
                          (shape_params['center_x'] - shape_params['width'] // 2,
                           shape_params['center_y'] - shape_params['height'] // 2),
                          (shape_params['center_x'] + shape_params['width'] // 2,
                           shape_params['center_y'] + shape_params['height'] // 2),
                          color=color,
                          thickness=-1)  # Filled rectangle
    return image
