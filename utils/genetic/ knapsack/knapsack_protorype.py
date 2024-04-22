import random
from PIL import Image, ImageDraw


class Item:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.value = self.value = self.calculate_value()
        self.start_row = None  # Row position on the grid
        self.start_col = None  # Column position on the grid

    # value is the surface area
    def calculate_value(self):
        return self.width * self.height


class Knapsack:
    def __init__(self, max_width, max_height):
        self.max_width = max_width
        self.max_height = max_height


# Represents a solution as a list of included items (0 - not included, 1 - included)
def create_chromosome(items):
    return [random.randint(0, 1) for _ in range(len(items))]


def can_place_item(item, knapsack_grid):
    for row in range(item.height):
        for col in range(item.width):
            # Assuming items are placed from the top-left
            grid_row = item.start_row + row
            grid_col = item.start_col + col

            if grid_row >= knapsack.max_height or grid_col >= knapsack.max_width:
                return False  # Out of bounds

            if knapsack_grid[grid_row][grid_col] != 0:
                return False  # Cell already occupied

    return True


def fitness(chromosome, items, knapsack):
    knapsack_grid = [[0 for _ in range(knapsack.max_width)] for _ in range(knapsack.max_height)]
    total_value = 0

    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            placed = False
            for row in range(knapsack.max_height):
                for col in range(knapsack.max_width):
                    items[i].start_row = row
                    items[i].start_col = col
                    if can_place_item(items[i], knapsack_grid):
                        # Place the item

                        for r in range(items[i].height):
                            for c in range(items[i].width):
                                knapsack_grid[r + row][c + col] = 1  # Mark as occupied
                        placed = True
                        total_value += items[i].value
                        break
                if placed:
                    break

            if not placed:
                return 0  # Invalid placement

    return total_value


# Mutation with a given probability
def mutate(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]  # Flip the bit


# Crossover of two parent chromosomes
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


# Main genetic algorithm function
def genetic_algorithm(items, knapsack, population_size, generations, mutation_rate):
    population = [create_chromosome(items) for _ in range(population_size)]

    for _ in range(generations):
        # Evaluate fitness of each chromosome
        fitness_scores = [fitness(chromosome, items, knapsack) for chromosome in population]

        # Select parents (we could use other selection mechanisms)
        parents = random.choices(population, weights=fitness_scores, k=population_size)

        # Create new generation through crossover and mutation
        new_population = []
        for i in range(0, population_size, 2):
            child1, child2 = crossover(parents[i], parents[i + 1])
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.append(child1)
            new_population.append(child2)

        population = new_population

    return max(population, key=lambda chromosome: fitness(chromosome, items, knapsack))


# Visualization Parameters
ITEM_COLOR = (255, 128, 0)  # Customize color for included items
BACKGROUND_COLOR = (255, 255, 255)
GRID_LINE_COLOR = (128, 128, 128)
CELL_SIZE = 50  # Size of each square representing a unit in the knapsack


def visualize_solution(chromosome, items, knapsack):
    image = Image.new('RGB', (knapsack.max_width * CELL_SIZE, knapsack.max_height * CELL_SIZE), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    # Draw Grid
    for x in range(0, knapsack.max_width * CELL_SIZE, CELL_SIZE):
        draw.line((x, 0, x, knapsack.max_height * CELL_SIZE), fill=GRID_LINE_COLOR)
    for y in range(0, knapsack.max_height * CELL_SIZE, CELL_SIZE):
        draw.line((0, y, knapsack.max_width * CELL_SIZE, y), fill=GRID_LINE_COLOR)

    # Draw items
    x_offset = 0
    y_offset = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            draw.rectangle([(x_offset, y_offset),
                            (x_offset + items[i].width * CELL_SIZE, y_offset + items[i].height * CELL_SIZE)],
                           fill=ITEM_COLOR)
        x_offset += items[i].width
        if x_offset >= knapsack.max_width:
            x_offset = 0
            y_offset += items[i].height

    image.show()


# Example Usage
items = [
    Item(3, 2),  # width, height
    Item(2, 4),
    Item(5, 3),
    Item(1, 2),
    Item(4, 1)
]

knapsack = Knapsack(10, 12)  # Only width and height constraints

# Genetic algorithm parameters
population_size = 50
generations = 1000
mutation_rate = 0.05

# Run the genetic algorithm
best_solution = genetic_algorithm(items, knapsack, population_size, generations, mutation_rate)

# Print the results
print("Best Solution (item indices included):", [i for i, x in enumerate(best_solution) if x == 1])

total_value = fitness(best_solution, items, knapsack)
print("Total Value:", total_value)

visualize_solution(best_solution, items, knapsack)
