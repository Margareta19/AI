
import random

# Genetic Algorithm for Delivery Route Optimisation
# Fixed random seed for reproducible results
random.seed(42)

# Distance matrix (kilometres)
locations = ["A", "B", "C", "D", "E", "F", "G"]

distance = {
    "A": {"A": 0, "B": 4, "C": 8, "D": 6, "E": 7, "F": 9, "G": 5},
    "B": {"A": 4, "B": 0, "C": 5, "D": 7, "E": 3, "F": 8, "G": 6},
    "C": {"A": 8, "B": 5, "C": 0, "D": 4, "E": 6, "F": 3, "G": 7},
    "D": {"A": 6, "B": 7, "C": 4, "D": 0, "E": 5, "F": 6, "G": 8},
    "E": {"A": 7, "B": 3, "C": 6, "D": 5, "E": 0, "F": 4, "G": 6},
    "F": {"A": 9, "B": 8, "C": 3, "D": 6, "E": 4, "F": 0, "G": 5},
    "G": {"A": 5, "B": 6, "C": 7, "D": 8, "E": 6, "F": 5, "G": 0}
}

# GA settings
POPULATION_SIZE = 100
GENERATIONS = 100
MUTATION_RATE = 0.10
ELITE_SIZE = 2
TOURNAMENT_SIZE = 5

# Each chromosome is a permutation of B, C, D, E, F and G.
# The depot A is added at the beginning and end.


def calculate_distance(chromosome):
    """Calculate the total route distance, including return to A."""
    route = ["A"] + chromosome + ["A"]
    total = 0

    for i in range(len(route) - 1):
        total += distance[route[i]][route[i + 1]]

    return total


def create_population():
    """Create an initial population of valid routes."""
    population = []

    for _ in range(POPULATION_SIZE):
        chromosome = ["B", "C", "D", "E", "F", "G"]
        random.shuffle(chromosome)
        population.append(chromosome)

    return population


def tournament_selection(population):
    """Select the route with the shortest distance from a random group."""
    contestants = random.sample(population, TOURNAMENT_SIZE)
    winner = min(contestants, key=calculate_distance)
    return winner.copy()


def order_crossover(parent1, parent2):
    """Order crossover (OX) preserves a valid permutation of locations."""
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]

    remaining = [
        gene for gene in parent2
        if gene not in child
    ]

    empty_positions = [
        i for i in range(size)
        if child[i] is None
    ]

    for position, gene in zip(empty_positions, remaining):
        child[position] = gene

    return child


def swap_mutation(chromosome):
    """Swap two locations to create a small route change."""
    mutated = chromosome.copy()

    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(mutated)), 2)
        mutated[i], mutated[j] = mutated[j], mutated[i]

    return mutated


def run_genetic_algorithm():
    """Run the genetic algorithm and return the best route."""
    population = create_population()
    best_route = None
    best_distance = float("inf")

    for generation in range(GENERATIONS):
        # Sort routes from shortest to longest
        population.sort(key=calculate_distance)

        # Update the best solution found so far
        if calculate_distance(population[0]) < best_distance:
            best_route = population[0].copy()
            best_distance = calculate_distance(best_route)

        # Keep the best individuals (elitism)
        new_population = [
            chromosome.copy()
            for chromosome in population[:ELITE_SIZE]
        ]

        # Generate the remaining population
        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            child = order_crossover(parent1, parent2)
            child = swap_mutation(child)

            new_population.append(child)

        population = new_population

    # Check the final population
    population.sort(key=calculate_distance)

    if calculate_distance(population[0]) < best_distance:
        best_route = population[0].copy()
        best_distance = calculate_distance(best_route)

    return best_route, best_distance


# Main program
if __name__ == "__main__":
    best_route, best_distance = run_genetic_algorithm()

    complete_route = ["A"] + best_route + ["A"]

    print("GENETIC ALGORITHM - DELIVERY ROUTE OPTIMISATION")
    print("-----------------------------------------------")
    print("Best delivery route:", " -> ".join(complete_route))
    print(f"Minimum total distance: {best_distance} km")
    print("Number of generations:", GENERATIONS)
    print("Population size:", POPULATION_SIZE)
    print("Random seed: 42")

    # Verify that every delivery location appears exactly once
    print("\nRoute validity check:")
    print("All locations visited once:",
          sorted(best_route) == sorted(["B", "C", "D", "E", "F", "G"]))
    print("Route starts and ends at depot A:",
          complete_route[0] == "A" and complete_route[-1] == "A")
