import random
import logging

logging.basicConfig(level=logging.INFO)


def generate_random_cities(cities_count: int = 50, x_range: tuple = (0, 100), y_range: tuple = (0, 100),
                           max_depth=5) -> list:
    """
    Generates a list of the desired number of random city coordinates with a recursive
    solution and a depth limit, ensuring that all the coordinates are unique.

    Args:
        cities_count: The number of cities to generate.
        x_range: A tuple representing the minimum and maximum x-coordinates (min_x, max_x).
        y_range: A tuple representing the minimum and maximum y-coordinates (min_y, max_y).
        max_depth: The maximum recursion depth to prevent infinite loops.

    Returns:
        A list of city coordinates, where each city is represented as a tuple (x, y),
        or None if unable to generate the desired number of unique cities within the depth limit.
    """

    generated_cities = set()
    while len(generated_cities) < cities_count:
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        generated_cities.add((x, y))

    if len(generated_cities) < cities_count and max_depth > 0:
        extra_needed = cities_count - len(generated_cities)
        x_diff, y_diff = x_range[1] - x_range[0], y_range[1] - y_range[0]
        new_cities = generate_random_cities(extra_needed,
                                            (x_range[0] - x_diff, x_range[1] + x_diff),
                                            (y_range[0] - y_diff, y_range[1] + y_diff),
                                            max_depth - 1)
        if new_cities is not None:
            generated_cities.update(new_cities)
        else:
            return None  # Failed to generate enough cities

    return list(generated_cities)[:cities_count]


def get_cities(number_of_cities: int = 10) -> list:
    """
    Returns a predefined list of city coordinates.
    Coordinates limits:
        x_range=(0, 100), y_range=(0, 100)

    Args:
        number_of_cities:
            if > 200, generates random coordinates

    Returns:
        A list of city coordinates, where each city is represented as a tuple (x, y)
    """
    if number_of_cities > 200:
        return generate_random_cities(number_of_cities)

    cities = [(26, 85), (73, 81), (89, 77), (90, 42), (71, 93), (28, 3), (14, 13), (54, 31), (73, 99), (63, 98),
              (77, 26), (66, 60), (30, 9), (84, 41), (82, 1), (12, 34), (54, 49), (94, 30), (13, 72), (18, 1),
              (58, 49), (13, 26), (36, 55), (59, 2), (79, 99), (16, 95), (93, 61), (62, 92), (9, 56), (19, 66),
              (62, 46), (30, 75), (7, 3), (27, 36), (67, 54), (58, 71), (40, 48), (52, 44), (53, 9), (26, 99),
              (47, 57), (9, 97), (31, 89), (54, 26), (17, 7), (93, 8), (20, 88), (76, 1), (51, 2), (32, 53),
              (75, 58), (94, 16), (66, 64), (89, 29), (57, 61), (38, 2), (52, 19), (52, 28), (33, 79), (8, 25),
              (10, 22), (35, 21), (87, 68), (25, 93), (82, 90), (62, 87), (49, 96), (56, 25), (32, 0), (12, 95),
              (84, 56), (61, 97), (72, 17), (7, 16), (76, 33), (16, 83), (19, 45), (54, 12), (70, 63), (45, 9),
              (31, 19), (51, 61), (78, 24), (80, 85), (75, 16), (98, 66), (32, 84), (48, 10), (7, 82), (49, 36),
              (4, 77), (96, 62), (9, 73), (98, 59), (52, 16), (1, 62), (44, 12), (79, 64), (48, 3), (25, 17), (9, 30),
              (74, 31), (19, 49), (6, 79), (77, 11), (97, 78), (9, 57), (35, 39), (68, 51), (53, 29), (3, 25),
              (60, 22), (55, 90), (36, 86), (2, 63), (59, 42), (36, 40), (85, 88), (62, 68), (44, 96), (74, 51),
              (65, 48), (20, 25), (92, 11), (26, 38), (18, 43), (79, 4), (10, 78), (45, 45), (25, 12), (48, 7),
              (3, 39), (9, 25), (29, 3), (86, 55), (62, 70), (83, 65), (6, 0), (80, 75), (97, 91), (30, 1), (6, 46),
              (19, 10), (62, 45), (54, 96), (30, 19), (73, 54), (36, 99), (83, 86), (94, 40), (12, 53), (6, 12),
              (48, 82), (12, 62), (32, 95), (32, 31), (32, 40), (75, 45), (52, 43), (21, 83), (59, 12), (61, 73),
              (74, 3), (71, 50), (62, 47), (90, 63), (73, 47), (65, 73), (3, 98), (82, 13), (20, 68), (31, 13),
              (49, 83), (75, 47), (31, 77), (60, 67), (93, 0), (36, 67), (39, 29), (26, 99), (33, 59), (36, 76),
              (19, 14), (27, 82), (73, 58), (76, 20), (76, 84), (26, 10), (29, 9), (15, 10), (50, 50), (98, 99),
              (43, 53), (70, 16), (2, 46), (90, 49), (78, 84), (47, 78), (92, 40), (75, 33)]
    return cities[:number_of_cities]


def generate_cities(cities_count: int = 50, random_cities: bool = False) -> list:
    logging.info("Generating {} cities".format(cities_count))
    if random_cities:
        cities = generate_random_cities(cities_count=cities_count)
        if cities is None:
            logging.warning("Failed to generate enough unique cities, using default list")
            cities = get_cities(cities_count)
        return cities
    else:
        return get_cities(cities_count)


def convert_string_routes(population):
    """Converts string representations of routes to lists of integers.

    Args:
        population: A list of strings representing routes (e.g., '["0", "4", ...]').

    Returns:
        A list of lists of integers representing the converted routes.
    """
    converted_population = []
    for route_string in population:
        # Remove square brackets and quotes
        route_string = route_string.strip('[]').replace('"', '')
        # Split the string by comma and convert each element to integer
        route_list = [int(element) for element in route_string.split(',')]
        converted_population.append(route_list)
    return converted_population
