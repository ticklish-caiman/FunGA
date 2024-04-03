import io

import matplotlib.pyplot as plt

from utils.genetic.tsp.tsp_operators import route_distance


# Visualization function
def plot_route(route, generation, cities, generations, pop_size, tournament_size, mutation_rate):
    plt.figure(figsize=(8, 6))
    x_coords = [cities[i][0] for i in route]
    y_coords = [cities[i][1] for i in route]
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])
    plt.plot(x_coords, y_coords, 'bo-')

    plt.scatter([city[0] for city in cities], [city[1] for city in cities], s=100, c='red')
    plot_title_left = f'Generation: {generation + 1}/{generations} ({((generation + 1) / generations) * 100:.0f}%)\nDistance: {route_distance(route, cities):.2f}\nCities: {len(cities)}'
    plot_title_right = f'Population size: {pop_size}\nTournament size: {tournament_size}\n Mutation rate: {mutation_rate}'
    font1 = {'family': 'serif', 'color': 'blue', 'size': 12}
    plt.title(
        plot_title_left, loc='left', fontdict=font1)
    plt.title(
        plot_title_right, loc='right', fontdict=font1)
    # plt.show()
    # Store the plot as an image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')  # Or 'jpeg'
    buffer.seek(0)
    image = buffer.getvalue()
    plt.close()  # Release the figure resources
    return image
