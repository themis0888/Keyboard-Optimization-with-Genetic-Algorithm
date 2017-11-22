from config import CONFIG
from GA_fitness import fitness
from solution import Solution
from random import random, uniform, randint

# random generation of population
def GA_initialization():
    return None

# select elite
def GA_selection():
    return None

# select two random parents for crossover
def GA_select_two_parents():
    return None

# crossover two parents
def GA_crossover(sol1, sol2):

    abo = CONFIG['letter_frequency']

    # Crossover method 1. with ordering based on frequency, just crossover
    # alpha : randomly choose
    alpha = randint(0, 25)
    new_pos1 = [(0, 0) for _ in range(27)]
    new_pos2 = [(0, 0) for _ in range(27)]
    get_index = lambda t:26 if t == ' ' else ord(t)-ord('a')

    for it, e in enumerate(' ' + abo): # ' ' means spacebar
        ind = get_index(e)
        if it < alpha:
            new_pos1[ind] = sol1.get_loc(ind)
            new_pos2[ind] = sol2.get_loc(ind)
        else:
            new_pos1[ind] = sol2.get_loc(ind)
            new_pos2[ind] = sol1.get_loc(ind)

    return Solution(new_pos1), Solution(new_pos2)

# mutate one individual, with the probability
def GA_mutation(sol):
    if random() > CONFIG['GA_mutation_rate']:
        return sol

    pos = sol.positions
    new_pos = []

    # Mutation method 1. change little bit on each poisition
    noise = CONFIG['GA_mutation_noise']
    for x, y in pos:
        new_pos.append((
            x + uniform(-noise, noise),
            y + uniform(-noise, noise) 
        ))
    # ISSUE: evaluate random float is much more time-consuming
    #   comparing with random int

    new_sol = Solution(new_pos) # ISSUE: Managing position outside of the field
    return new_sol

# run genetic algorithm
def run_GA():
    # initialization
    current_population = GA_initialization()

    # iteration for generations
    for num_gen in range(CONFIG['GA_num_generation']):
        # empty population for next generation
        next_population = []

        # add elite from current population
        next_population += GA_selection(current_population)

        # fill next population with offsprings
        while len(next_population) == CONFIG['GA_num_population']:
            # crossover
            left, right = GA_select_two_parents(current_population)
            left_offspring, right_offspring = GA_crossover(left, right)

            # mutation
            left_offspring = GA_mutation(left_offspring)
            right_offsprin = GA_mutation(right_offspring)
            next_population += [left_offspring, right_offspring]

        # generation chane
        current_population = next_population

    return current_population