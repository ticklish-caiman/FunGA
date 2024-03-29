import math

from utils.genetic.biomorphs.genes import generate_random_genes


class Biomorph:
    """Represents a single biomorph creature."""

    def __init__(self, size=None):
        """Initializes a Biomorph with default settings."""
        self.body = None
        self.head = None
        self.left_eye = None
        self.right_eye = None
        self.legs = []
        # self.leg_segments = leg_segments
        self.color = None
        self.genes = None
        self.size = size
        self.fitness = None
        self.chosen_one = False
        # TODO: maybe store the PIL img data inside the object?

    def generate_biomorph(self):
        """Generates a complete Biomorph based on provided genes or random defaults."""
        if self.genes is None:
            self.genes = generate_random_genes()

        if self.color is None:
            self.color = self.genes['color']

        if self.size is None:
            self.size = (500, 500)

        self.body = self.generate_body(self.genes['body_radius'])
        self.head, self.left_eye, self.right_eye = self.generate_head(self.genes['head_radius'])

        for angle_index in range(self.genes['leg_count']):
            self.generate_leg(self.body['x1'] + self.body['width'] / 2,
                              self.body['y1'] + self.body['height'] / 2,
                              self.genes['leg_count'], self.genes['leg_width'], angle_index,
                              self.genes['offset_angle'])

    def generate_body(self, body_radius, start_x=None, start_y=None):
        """Generates the body of the Biomorph."""
        if start_x is None or start_y is None:
            start_x, start_y = self.size[0]/2, self.size[1]/2

        body = ({'type': 'ellipse',
                 'x1': start_x - body_radius,
                 'y1': start_y - body_radius,
                 'width': body_radius * 2,
                 'height': body_radius * 2,
                 'color': self.color})
        return body

    def generate_leg(self, start_x, start_y, leg_segments, leg_width, angle_index, offset_angle):
        if leg_segments == 0:
            # Generate foot
            foot_radius = 10
            last_x, last_y = self.legs[-1]['x2'], self.legs[-1]['y2']
            self.legs.append({
                'type': 'ellipse',
                'x1': last_x - foot_radius,
                'y1': last_y - foot_radius,
                'width': foot_radius * 2,
                'height': foot_radius * 2,
                'color': self.color
            })
        else:
            self.legs.append(self.generate_leg_segment(start_x, start_y, leg_width, angle_index, offset_angle))
            last_part = self.legs[-1]
            self.generate_leg(last_part['x2'], last_part['y2'], leg_segments - 1, leg_width, angle_index, offset_angle)

    def generate_leg_segment(self, start_x=None, start_y=None, leg_width=1, angle_index=0, segment_offset_angle=0):
        """Generates a single leg segment."""
        # Calculate angle in degrees directly
        angle_degrees = angle_index
        # Optionally offset all legs by some amount for different poses
        angle_degrees += segment_offset_angle / 10

        length = 40
        end_x = int(start_x + length * math.cos(angle_degrees))
        end_y = int(start_y + length * math.sin(angle_degrees))
        leg_segment = ({'type': 'line',
                        'x1': start_x, 'y1': start_y,
                        'x2': end_x, 'y2': end_y,
                        'width': leg_width,
                        'color': self.color})
        return leg_segment

    def generate_head(self, head_radius):
        """Generates the head and eyes of the Biomorph."""
        if self.body is None:
            raise ValueError("Cannot generate head without a body")

        head_x = self.body['x1'] + (self.body['width'] / 2)
        head_y = self.body['y1'] - head_radius

        eye_radius = head_radius * 0.1
        eye_offset_x = head_radius * 0.3
        eye_offset_y = head_radius * 0.3

        head = {'type': 'ellipse',
                'x1': head_x - head_radius,
                'y1': head_y - head_radius,
                'width': head_radius * 2,
                'height': head_radius * 2,
                'color': self.color}

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

        return head, left_eye, right_eye
