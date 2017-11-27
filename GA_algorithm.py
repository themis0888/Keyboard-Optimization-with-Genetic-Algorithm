from config import CONFIG
from GA_fitness import fitness
from solution import Solution
from random import random, uniform, randint, choice
import numpy as np

# random generation of population
def GA_initialization():
    current_population = []

    for i in range(CONFIG['GA_num_population']):
        current_population.append(Solution())

    return current_population

# select elite
def GA_selection(population):
    sorted_population = sorted(population, key=fitness)
    return sorted_population[:CONFIG['GA_num_selection']]

# select two random parents for crossover
def GA_select_two_parents(population):
    return choice(population), choice(population)

# crossover two parents
def GA_crossover(sol1, sol2):

    abo = CONFIG['letter_frequency']

    # Crossover method 1. with ordering based on frequency, just crossover
    # CUTOFF alpha : randomly choose
    # DEAD METHOD, since it does not seems to generate better result
    if False:
        alpha = randint(0, 24)
        new_pos1 = [(0, 0) for _ in range(27)]
        new_pos2 = [(0, 0) for _ in range(27)]
        get_index = lambda t:ord(t)-ord('a')

        for it, e in enumerate(abo):
            ind = get_index(e)
            if it < alpha:
                new_pos1[ind] = sol1.get_loc(ind)
                new_pos2[ind] = sol2.get_loc(ind)
            else:
                new_pos1[ind] = sol2.get_loc(ind)
                new_pos2[ind] = sol1.get_loc(ind)

    # Crossover method 2, idea by BJ
    # offspring1 : given location information from parent 1
    #              given alphabet information from parent 2
    #                              ordering from left to right
    # offspring2 : given location information from parent 2
    #              given alphabet information from parent 1
    #                              ordering from left to right
    # ISSUE: Some limitation on searching for solution space?
    # ISSUE: Is it generate better result?
    def crossover2(pos1, pos2):
        assert pos1.shape[1] == 2 == pos2.shape[1]

        # ordering information
        # if p1 = [1, 3, 2, 0] means
        #   among b(1), d(3), c(2), a(0),
        #   b is on the leftmost side, a is on the rightmost side
        p1 = np.argsort(pos1[:,0]) # pos1[p1[i]][0] < pos1[p1[i+1]][0]
        p2 = np.argsort(pos2[:,0])

        new_pos1 = np.zeros(pos1.shape)
        new_pos2 = np.zeros(pos2.shape)

        # alphabet with index ai is i'th in new_pos2
        for i, ai in enumerate(p2):
            new_pos1[ai] = pos1[p1[i]]

        for j, aj in enumerate(p1):
            new_pos2[aj] = pos2[p2[j]]

        return new_pos1, new_pos2

    a, b = crossover2(
        np.array([
            [0, 0],
            [1, 0],
            [0.4, 0],
            [7, 0]]),
        np.array([
            [2, 0],
            [4, 0],
            [1.5, 0],
            [1, 0]]))
    assert  np.all(a == np.array([
            [1, 0],
            [7, 0],
            [0.4, 0],
            [0, 0]]))
    assert np.all(b ==  np.array([
            [1, 0],
            [2, 0],
            [1.5, 0],
            [4, 0]]))
    if True:
        new_pos1, new_pos2 = crossover2(sol1.positions, sol2.positions)

    return Solution(new_pos1), Solution(new_pos2)

# mutate one individual, with the probability
def GA_mutation(sol):
    if random() > CONFIG['GA_mutation_rate']:
        return sol

    pos = sol.positions
    new_sol = None

    if randint(0, 1): # 0 for 50%, 1 for 50%
        # Mutation method 1. change little bit on each poisition
        new_pos = []

        noise = CONFIG['GA_mutation_noise']

        width, height = Solution.field.width, Solution.field.height
        for x, y in pos:
            new_x = x + uniform(-noise, noise)
            new_y = y + uniform(-noise, noise)

            if new_x < 0:
                new_x = 0
            if new_x > width:
                new_x = width

            if new_y < 0:
                new_y = 0
            elif new_y > height:
                new_y = height

            new_pos.append((new_x, new_y))
        # ISSUE: evaluate random float is much more time-consuming
        #   comparing with random int

        new_sol = Solution(new_pos)

    else:
        # Mutation method 2. Swap two points, with specific rate.
        # If swapped for one time, check for one more time with same rate.
        # Repeat swapping until the swapping limit is reached.
        for i in range(CONFIG['GA_mutation_swap_limit']):
            if random() > CONFIG['GA_mutation_swap_rate']:
                break

            # randomly choose two indexes
            assert len(pos) == 26, "Error on implementation"
            i = randint(0, len(pos)-1) # probably, len(pos) == 26
            j = randint(0, len(pos)-2)
            #print(i, j)
            if j >= i:
                j = j+1

            # SWAP VERIFIED (with some experiment)
            a, b = pos[j].copy(), pos[i].copy()
            pos[i], pos[j] = a, b


        new_sol = Solution(pos)

    return new_sol

# run genetic algorithm
def run_GA():
    # initialization
    current_population = GA_initialization()

    # iteration for generations
    for num_gen in range(CONFIG['GA_num_generation']):
        print('GEN', num_gen)
        # empty population for next generation
        next_population = []

        # add elite from current population
        next_population += GA_selection(current_population)

        # fill next population with offsprings
        while len(next_population) != CONFIG['GA_num_population']:
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