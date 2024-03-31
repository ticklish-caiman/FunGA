import matplotlib.pyplot as plt

from utils.genetic.tsp.tsp_operators import route_distance


# Visualization function
def plot_route(route, iterations, cities):
    plt.figure(figsize=(8, 6))
    x_coords = [cities[i][0] for i in route]
    y_coords = [cities[i][1] for i in route]
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])
    plt.plot(x_coords, y_coords, 'bo-')

    plt.scatter([city[0] for city in cities], [city[1] for city in cities], s=100, c='red')
    plt.title(f'Iteration: {iterations} - Distance: {route_distance(route):.2f}')
    plt.show()
