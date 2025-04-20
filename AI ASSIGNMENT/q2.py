import random
import numpy as np
task_times = [3, 2, 4, 6, 5, 8, 7] 
capacities = [24, 30, 28]  
cost_matrix = [  
    [10, 12, 14],
    [9, 10, 13],
    [8, 11, 9],
    [14, 12, 10],
    [13, 10, 12],
    [12, 13, 11],
    [11, 12, 13]
]

n_tasks = len(task_times)
n_facilities = len(capacities)
population_size = 50
generations = 200
mutation_rate = 0.1
tournament_size = 3
def fitness(individual):
    total_cost = 0
    facility_time = [0] * n_facilities

    for task, facility in enumerate(individual):
        time = task_times[task]
        cost = cost_matrix[task][facility]
        total_cost += time * cost
        facility_time[facility] += time

    penalty = 0
    for f in range(n_facilities):
        if facility_time[f] > capacities[f]:
            penalty += (facility_time[f] - capacities[f]) * 100  

    return total_cost + penalty
def generate_individual():
    return [random.randint(0, n_facilities - 1) for _ in range(n_tasks)]

def generate_population():
    return [generate_individual() for _ in range(population_size)]
def tournament_selection(pop):
    best = None
    for _ in range(tournament_size):
        ind = random.choice(pop)
        if best is None or fitness(ind) < fitness(best):
            best = ind
    return best
def crossover(parent1, parent2):
    point = random.randint(1, n_tasks - 1)
    return parent1[:point] + parent2[point:]

def mutate(individual):
    for i in range(n_tasks):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, n_facilities - 1)
    return individual

def genetic_algorithm():
    population = generate_population()
    best_solution = None

    for gen in range(generations):
        new_population = []
        for _ in range(population_size):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population
        best_in_gen = min(population, key=fitness)
        if best_solution is None or fitness(best_in_gen) < fitness(best_solution):
            best_solution = best_in_gen

        print(f"Generation {gen+1}: Best Cost = {fitness(best_solution)}")

    return best_solution
solution = genetic_algorithm()
print("\nBest Assignment (Task -> Facility):")
for i, facility in enumerate(solution):
    print(f"Task {i+1} -> Facility {facility+1}")
print(f"\nMinimum Cost: {fitness(solution)}")
