import random


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


def get_cities(number_of_cities: int = 10):
    """
    Returns a predefined list of city coordinates.
    Coordinates limits:
        x_range=(0, 100), y_range=(0, 100)

    Args:
        number_of_cities: 10, 20, 50, 100, 200
            if None, returns all cities 10 cities

    Returns:
        A list of city coordinates, where each city is represented as a tuple (x, y)
    """
    if number_of_cities == 10:
        return [(89, 55), (44, 99), (28, 28), (93, 29), (1, 13), (14, 80), (20, 93), (60, 67), (1, 90), (19, 60)]
    elif number_of_cities == 20:
        return [(89, 13), (30, 55), (4, 76), (54, 92), (38, 44), (4, 88), (34, 40), (67, 70), (34, 67), (94, 8),
                (96, 2), (1, 60), (37, 44), (88, 86), (57, 86), (9, 46), (49, 88), (35, 98), (5, 26), (11, 88)]
    elif number_of_cities == 50:
        return [(32, 40), (45, 77), (41, 58), (95, 96), (4, 15), (46, 54), (71, 47), (2, 51), (50, 18), (69, 28),
                (98, 64), (64, 50), (56, 55), (89, 61), (83, 51), (81, 23), (73, 19), (21, 76), (24, 32), (27, 55),
                (69, 64), (12, 18), (10, 5), (56, 39), (11, 65), (50, 81), (4, 87), (43, 75), (15, 53), (13, 65),
                (94, 90), (27, 33), (55, 49), (49, 67), (66, 22), (19, 99), (66, 49), (46, 98), (55, 76), (48, 73),
                (51, 2), (26, 49), (48, 49), (35, 6), (91, 87), (35, 70), (83, 89), (82, 8), (0, 88), (16, 78)]
    elif number_of_cities == 100:
        return [(59, 55), (99, 36), (90, 33), (93, 50), (20, 93), (8, 73), (9, 17), (74, 18), (46, 66), (50, 27),
                (82, 86), (10, 54), (29, 34), (73, 46), (13, 65), (50, 38), (70, 4), (19, 50), (83, 62), (52, 19),
                (33, 79), (35, 21), (48, 15), (1, 28), (5, 53), (2, 45), (97, 35), (33, 72), (26, 66), (88, 90),
                (60, 55), (91, 70), (66, 77), (6, 65), (27, 51), (77, 64), (66, 98), (86, 76), (51, 54), (51, 8),
                (41, 7), (70, 22), (79, 55), (70, 95), (98, 22), (18, 11), (83, 34), (97, 5), (89, 83), (45, 34),
                (99, 69), (24, 75), (25, 83), (92, 48), (46, 26), (2, 90), (6, 17), (37, 66), (5, 70), (28, 20),
                (71, 55), (86, 64), (97, 82), (98, 56), (58, 84), (21, 99), (99, 0), (89, 32), (70, 92), (50, 89),
                (22, 36), (5, 93), (22, 54), (11, 97), (77, 8), (43, 49), (89, 16), (26, 97), (1, 6), (56, 49),
                (25, 80), (75, 84), (46, 78), (75, 93), (33, 68), (51, 76), (51, 85), (20, 6), (23, 2), (40, 82),
                (52, 47), (58, 8), (17, 1), (25, 48), (1, 1), (56, 90), (1, 65), (40, 48), (85, 89), (32, 83)]

    elif number_of_cities == 200:
        return [(26, 85), (73, 81), (89, 77), (90, 42), (71, 93), (28, 3), (14, 13), (54, 31), (73, 99), (63, 98),
                (77, 26), (66, 60), (30, 9), (84, 41), (82, 1), (12, 34), (54, 49), (94, 30), (13, 72), (18, 1),
                (58, 49), (13, 26), (36, 55), (59, 2), (79, 99), (16, 95), (93, 61), (62, 92), (9, 56), (19, 66),
                (62, 46), (30, 75), (7, 3), (27, 36), (67, 54), (58, 51), (60, 48), (52, 44), (53, 9), (26, 89),
                (47, 57), (16, 97), (31, 79), (54, 26), (17, 7), (93, 8), (20, 88), (76, 1), (51, 2), (32, 53),
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


# cities = generate_random_cities()
cities = get_cities(50)
print(cities)

if cities is None:
    print("Failed to generate enough unique cities, using default list")
    cities = get_cities()
