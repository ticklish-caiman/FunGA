import io

import matplotlib.pyplot as plt

from utils.genetic.tsp.tsp_operators import route_distance


# Visualization function
def plot_route(route, generation, cities, generations):
    plt.figure(figsize=(8, 6))
    x_coords = [cities[i][0] for i in route]
    y_coords = [cities[i][1] for i in route]
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])
    plt.plot(x_coords, y_coords, 'bo-')

    plt.scatter([city[0] for city in cities], [city[1] for city in cities], s=100, c='red')
    plt.title(
        f'Generation: {generation + 1}/{generations} ({((generation + 1) / generations) * 100:.0f}%)\nDistance: {route_distance(route, cities):.2f}\nCities:{len(cities)}')
    # plt.show()
    # Store the plot as an image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')  # Or 'jpeg'
    buffer.seek(0)
    image = buffer.getvalue()
    plt.close()  # Release the figure resources
    return image
