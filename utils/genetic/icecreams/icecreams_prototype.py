import random

# Ingredient costs
FLAVOR_COSTS = {
    "chocolate": 0.5, "vanilla": 0.4, "raspberry": 0.8, "strawberry": 0.7,
    "pistachio": 1.0, "coffee": 0.6
}
PACKAGE_COSTS = {"waffle": 0.6, "cup": 0.3}
EXTRA_COSTS = {"chocolate topping": 0.3, "fruit mix": 0.5, "nuts": 0.4}

# Markups
FLAVOR_MARKUPS = {
    "chocolate": 1.2, "vanilla": 1.0, "raspberry": 1.5, "strawberry": 1.3,
    "pistachio": 1.6, "coffee": 1.1
}
PACKAGE_MARKUPS = {"waffle": 1.15, "cup": 1.0}  # Multiply selling price based on package
EXTRA_MARKUPS = [1.1, 1.3, 1.2]


def create_chromosome():
    """Creates a random ice cream configuration."""
    flavor = random.choices(list(FLAVOR_COSTS.keys()), weights=list(FLAVOR_MARKUPS.values()))[
        0]  # Biased towards higher markups
    package = random.choices(list(PACKAGE_COSTS.keys()), weights=list(PACKAGE_MARKUPS.values()))[0]
    extras = random.sample(list(EXTRA_COSTS.keys()), random.randint(1, len(EXTRA_COSTS)))  # Always at least one extra
    return {"flavor": flavor, "package": package, "extras": extras}


def calculate_cost(ice_cream_config):
    cost = 0
    cost += FLAVOR_COSTS[ice_cream_config['flavor']]
    cost += PACKAGE_COSTS[ice_cream_config['package']]
    for extra in ice_cream_config['extras']:
        cost += EXTRA_COSTS[extra]
    return cost


def calculate_markup(ice_cream_config):
    markup = FLAVOR_MARKUPS[ice_cream_config['flavor']]
    markup *= PACKAGE_MARKUPS[ice_cream_config['package']]
    for i, extra in enumerate(ice_cream_config['extras']):
        markup *= EXTRA_MARKUPS[i]
    return markup


def fitness(chromosome):
    selling_price = calculate_markup(chromosome)
    cost = calculate_cost(chromosome)
    return selling_price - cost


def mutate(chromosome):
    mutation_type = random.choice(["flavor", "package", "extras"])
    if mutation_type == "flavor":
        chromosome['flavor'] = random.choice(list(FLAVOR_COSTS.keys()))
    elif mutation_type == "package":
        chromosome['package'] = random.choice(list(PACKAGE_COSTS.keys()))
    else:  # extras
        if random.random() < 0.5:  # Add an extra
            new_extra = random.choice(list(EXTRA_COSTS.keys()))
            if new_extra not in chromosome['extras']:
                chromosome['extras'].append(new_extra)
        else:  # Remove an extra
            if chromosome['extras']:  # Check if extras exist
                chromosome['extras'].pop(random.randrange(len(chromosome['extras'])))


def crossover(parent1, parent2):
    # Swap 'package' type
    child1 = parent1.copy()
    child2 = parent2.copy()
    child1["package"] = parent2["package"]
    child2["package"] = parent1["package"]

    # Merge extras with a check to avoid exact duplicates
    child1['extras'] = list(set(child1['extras'] + parent2['extras']))
    child2['extras'] = list(set(child2['extras'] + parent1['extras']))

    return child1, child2


# Run the genetic algorithm
def genetic_algorithm(population_size, generations, mutation_rate, elitism_rate):
    """Runs the genetic algorithm with the specified parameters and elitism."""

    # Initialize population
    population = [create_chromosome() for _ in range(population_size)]

    for generation in range(generations):
        # Evaluate fitness and sort (crucial for elitism)
        population = sorted(population, key=fitness, reverse=True)

        # Elitism: Keep the top individuals unchanged
        num_elites = int(elitism_rate * population_size)
        new_population = population[:num_elites]

        # Select parents (tournament selection) for the rest
        parents = []
        for _ in range(population_size - num_elites):
            # Only select from the non-elite part
            competitor1 = random.choice(population[num_elites:])
            competitor2 = random.choice(population[num_elites:])
            parents.append(competitor1 if fitness(competitor1) > fitness(competitor2) else competitor2)

        # Create the remaining offspring through crossover and mutation
        for i in range(0, len(parents), 2):
            child1, child2 = crossover(parents[i], parents[i + 1])
            if random.random() < mutation_rate:
                mutate(child1)
            if random.random() < mutation_rate:
                mutate(child2)
            new_population.append(child1)
            new_population.append(child2)

        population = new_population

    # After all generations, return the best solution
    return max(population, key=fitness)


# Find and display the most profitable ice cream configuration
# Genetic algorithm parameters
population_size = 50
generations = 100
mutation_rate = 0.1
elitism_rate = 0.05  # Keep 5% of the population as elites

# Run the genetic algorithm and get the best solution
best_solution = genetic_algorithm(population_size, generations, mutation_rate, elitism_rate)

print("\nBest Ice Cream Configuration:")
print(best_solution)
print("Profit:", fitness(best_solution))
