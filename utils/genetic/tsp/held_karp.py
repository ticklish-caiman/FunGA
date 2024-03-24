import math
from itertools import combinations

# Held-Karp approach might be used to evaluate how good the GA did
# Can't get it to work thou, so for now visual inspection will do

# City representation
cities = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3)]


# Distance calculation
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# Held-Karp Algorithm with Debugging
def held_karp(cities):
    n = len(cities)

    # Cache initialization
    cache = {}
    for k in range(1, n):
        cache[(1 << k, k)] = (distance(cities[0], cities[k]), 0)

        # Subset iteration + calculations
    for subset_size in range(2, n):
        for subset in combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            for k in subset:
                prev = bits & ~(1 << k)

                min_cost = float('inf')
                for prev_city in subset:
                    if prev_city != k:
                        cost = cache[(prev, prev_city)][0] + distance(cities[prev_city], cities[k])
                        min_cost = min(min_cost, cost)

                # Debugging: Print key values and calculations
                print(f"\nSubset bitmask: {bits}, k: {k}")
                print(f"prev: {prev}")
                print(f"Calculated min_cost: {min_cost}")

                cache[(bits, k)] = (min_cost, prev_city)

    bits = (2 ** n - 1) - 1
    optimal_cost = float('inf')
    last_city = -1

    for k in range(1, n):
        cost = cache[(bits, k)][0] + distance(cities[k], cities[0])
        if cost < optimal_cost:
            optimal_cost = cost
            last_city = k

    path = [0]
    for i in range(n - 1):
        path.append(last_city)
        new_bits = bits & ~(1 << last_city)

        print(f"bits: {bits}, new_bits: {new_bits}, last_city: {last_city}")

        if (new_bits, last_city) not in cache:
            print(f"KeyError: Key ({new_bits}, {last_city}) not found in cache!")

        _, last_city = cache[(new_bits, last_city)]
    path.append(0)
    path.reverse()

    return path, optimal_cost


# Example
best_path, cost = held_karp(cities)
print(f"Held-Karp optimal TSP route: {best_path}")
print(f"Total distance: {cost}")
