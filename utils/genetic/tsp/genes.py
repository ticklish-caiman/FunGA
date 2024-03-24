import random


def get_cities():
    return [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3), (4, 6), (11, 5)]


def generate_random_cities(num_cities=50, x_range=(0, 100), y_range=(0, 100), max_depth=5):
    """
    Generates a list of the desired number of random city coordinates with a recursive
    solution and a depth limit, ensuring that all the coordinates are unique.

    Args:
        num_cities: The number of cities to generate.
        x_range: A tuple representing the minimum and maximum x-coordinates (min_x, max_x).
        y_range: A tuple representing the minimum and maximum y-coordinates (min_y, max_y).
        max_depth: The maximum recursion depth to prevent infinite loops.

    Returns:
        A list of city coordinates, where each city is represented as a tuple (x, y),
        or None if unable to generate the desired number of unique cities within the depth limit.
    """

    generated_cities = set()
    while len(generated_cities) < num_cities:
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        generated_cities.add((x, y))

    if len(generated_cities) < num_cities and max_depth > 0:
        extra_needed = num_cities - len(generated_cities)
        x_diff, y_diff = x_range[1] - x_range[0], y_range[1] - y_range[0]
        new_cities = generate_random_cities(extra_needed,
                                            (x_range[0] - x_diff, x_range[1] + x_diff),
                                            (y_range[0] - y_diff, y_range[1] + y_diff),
                                            max_depth - 1)
        if new_cities is not None:
            generated_cities.update(new_cities)
        else:
            return None  # Failed to generate enough cities
    return list(generated_cities)[:num_cities]


cities = generate_random_cities()

if cities is None:
    print("Failed to generate enough unique cities, using default list")
    cities = get_cities()
