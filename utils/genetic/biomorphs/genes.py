import random

genes = {
    'body_radius': 50,  # Controls the size of the body
    'head_radius': 40,
    'leg_count': 4,
    'leg_segments': 4,
    'leg_width': 3,  # Base width of legs
    'leg_width_variation': 2,  # How much leg width can vary across segments
    'color': 'red',  # Could be a simple color name, or RGB tuple
}


def generate_random_genes():
    return {
        'body_radius': random.randint(40, 60),
        'head_radius': random.randint(20, 40),
        'leg_count': random.randint(4, 4),
        'leg_segments': random.randint(3, 5),
        'leg_width': random.randint(2, 15),
        'leg_width_variation': random.randint(1, 2000),
        'color': random.choice(['red', 'green', 'blue']),
        'angle': random.randint(0, 6)
    }
