import logging
import random
import cv2
import numpy as np

from utils.genetic.shapevo_alternative.alt_shapevo_phenotype import generate_image_opencv

logging.basicConfig(level=logging.INFO)


def calculate_fitness(image):
    # 1. Edge Complexity
    edges = cv2.Canny(image, *image.shape)  # Adjust thresholds for desired edge detection
    # cv2.imshow("Edges", edges)
    # cv2.waitKey(0)
    edge_density = np.sum(edges > 0) / (image.shape[0] * image.shape[1])

    fitness = edge_density
    print('Fitness: {}'.format(fitness))
    return fitness


class Shape:
    def __init__(self, image_width, image_height, max_num_shapes=5):
        self.image_width = image_width
        self.image_height = image_height
        self.max_num_shapes = max_num_shapes
        self.genome = None
        self.rendered_image = None
        self.fitness = None

    def render_shape(self):
        self.rendered_image = generate_image_opencv(self.genome, self.image_width, self.image_height)

    def calculate_fitness(self):
        if self.rendered_image is None:
            raise ValueError("Image needs to be rendered before calculating fitness")

        self.fitness = calculate_fitness(self.rendered_image)

    def display(self):
        if self.rendered_image is None:
            self.render_shape()  # Ensure the image is rendered
        cv2.imshow("Shape", self.rendered_image)
        cv2.waitKey(0)  # Wait for a keypress to close the window
        cv2.destroyAllWindows()

    def generate_genome(self, max_num_shapes=5):
        genome = []
        num_shapes = random.randint(1, max_num_shapes)
        for _ in range(num_shapes):
            shape_type = random.choice(['circle', 'rectangle'])
            center_x = random.randint(10, self.image_width - 11)
            center_y = random.randint(0, self.image_height - 1)

            if shape_type == 'circle':
                # Ensure radius fits within image bounds
                max_radius = min(center_x, center_y, self.image_width - center_x, self.image_height - center_y)
                logging.info('Max radius: {}'.format(max_radius))
                radius = random.randint(1, max_radius)
                shape_params = {'type': shape_type, 'center_x': center_x, 'center_y': center_y, 'radius': radius}
            else:
                width = random.randint(20, self.image_width // random.randint(3, 10))
                height = random.randint(20, self.image_height // random.randint(3, 10))
                shape_params = {'type': shape_type, 'center_x': center_x, 'center_y': center_y, 'width': width,
                                'height': height}

            genome.append(shape_params)

        self.genome = genome

# shape_test = Shape(200, 200, max_num_shapes=5)
# shape_test.render()
# shape_test.calculate_fitness()
# print(shape_test.fitness)
# print(shape_test.rendered_image)
# shape_test.display()
