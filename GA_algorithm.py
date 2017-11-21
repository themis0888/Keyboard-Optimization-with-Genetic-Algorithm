from config import CONFIG
from GA_fitness import fitness

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
def GA_crossover():
    return None

# mutate one individual
def GA_mutation():
    return None

# run genetic algorithm
def run_GA():
    # initialization
    current_population = initialization()

    # iteration for generations
    for num_gen in range(CONFIG['GA_num_generation']):
        # empty population for next generation
        next_population = []

        # add elite from current population
        next_population.extend(GA_selection(current_population))

        # fill next population with offsprings
        while len(next_population) == CONFIG['GA_num_population']:
            # crossover
            left, right = GA_select_two_parents(current_population)
            left_offspring, right_offspring = crossover(left, right)

            # mutation
            left_offspring = mutation(left_offspring)
            right_offsprin = mutation(right_offspring)
            next_population.extend([left_offspring, right_offspring])

        # generation chane
        current_population = next_population

    return current_population