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
    import sys
    assert sys.version_info[0] == 3, sys.version_info

    abo = CONFIG['letter_frequency']
    get_index = lambda t:ord(t)-ord('a')

    # Crossover method 1. with ordering based on frequency, just crossover
    # CUTOFF alpha : randomly choose
    # DEAD METHOD, since it does not seems to generate better result
    if False:
        alpha = randint(0, 24)
        new_pos1 = [(0, 0) for _ in range(26)]
        new_pos2 = [(0, 0) for _ in range(26)]

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

    # Crossover method 3, idea by BS
    # offspring1 : given left-half location from parent 1
    #              given right-half location from parent 2
    # offspring2 : given left-half location from parent 2
    #              given right-half location from parent 1
    # alphabet information on each offspring
    #    -> depending on priority on alphabet frequency
    #
    # ISSUE: Is it generate better result?
    def crossover3(pos1, pos2):
        assert len(pos1) == len(pos2) == 26

        # ordering information
        # if p1 = [1, 3, 2, 0] means
        #   among b(1), d(3), c(2), a(0),
        #   b is on the leftmost side, a is on the rightmost side
        p1 = np.argsort(pos1[:,0]) # pos1[p1[i]][0] < pos1[p1[i+1]][0]
        p2 = np.argsort(pos2[:,0])

        # ISSUE: overlapping problem.
        # For each parent, one point in parent and other one in other parent
        #   could be 'close' to each other. These pairs of points should not
        #   reach to single offspring.
        # Dividing into two parts for each parent, making no overlapping points.
        # ASSUMPTION: there is no two close points in one parent
        # The assumption is not really critical, but it helps thinking
        close = lambda pos1, pos2: \
            np.abs(pos1[0]-pos2[0]) < 0.01 and \
            np.abs(pos1[1]-pos2[1]) < 0.01

        # Extract close points iteratively.
        overlapped = [] # tuple of (idx1, idx2)
        for idx1 in p1:
            point1 = pos1[idx1]

            for idx2 in p2:
                point2 = pos2[idx2]
                if close(point1, point2):
                    overlapped.append((idx1, idx2))
                    break
                if point2[0] > point1[0] + 0.01:
                    break

        # Below statements are used before fixing overlapping issue
        # p1_left_pos_idx = p1[:13]
        # p1_right_pos_idx = p2[13:]
        # p2_left_pos_idx = p2[:13]
        # p2_right_pos_idx = p1[13:]

        # Step 1. Divide overlapped points into two part
        #   with ordering left to right
        #   (may be not exactly half for odd)
        # Step 2. Divide remaining points into two parts
        #   with ordering left to right
        p1_left_pos_idx  = []  # left part of offspring 1
        p1_right_pos_idx = []  # right part of offspring 2
        p2_left_pos_idx  = []  # left part of offspring 2
        p2_right_pos_idx = []  # right part of offspring 1

        # Step 1
        half = len(overlapped) // 2
        for i, (idx1, idx2) in enumerate(overlapped):
            if i < half:
                p1_left_pos_idx.append(idx1)
                p2_left_pos_idx.append(idx2)
            else:
                p1_right_pos_idx.append(idx1)
                p2_right_pos_idx.append(idx2)

        p1_used_idx = p1_left_pos_idx + p1_right_pos_idx
        p2_used_idx = p2_left_pos_idx + p2_right_pos_idx

        # Step 2
        for idx in p1:
            if idx not in p1_used_idx:
                if len(p1_left_pos_idx) < 13:
                    p1_left_pos_idx.append(idx)
                else:
                    p1_right_pos_idx.append(idx)
        for idx in p2:
            if idx not in p2_used_idx:
                if len(p2_left_pos_idx) < 13:
                    p2_left_pos_idx.append(idx)
                else:
                    p2_right_pos_idx.append(idx)

        assert len(p1_left_pos_idx) == 13
        assert len(p1_right_pos_idx) == 13
        assert len(p2_left_pos_idx) == 13
        assert len(p2_right_pos_idx) == 13

        new_pos1 = np.zeros(pos1.shape)
        new_pos2 = np.zeros(pos2.shape)

        # decide which part to go when alphabet ALPHA given
        # case 1. ALPHA is on the left on parent 1 and
        #         ALPHA is on the left on parent 2
        #   -> put ALPHA on just corresponding location on offsprings 1
        # case 2. ALPHA is on the right on parent 1 and
        #         ALPHA is on the right on parent 2
        #   -> just same as case 1.
        # case 3. ALPHA is on the left on parent 1 and
        #         ALPHA is on the right on parent 2
        #   -> Both corresponding locations are on the offspring 1
        #   -> Yield one between them, for some another alphabet,
        #      which assigned to both location on offspring 2
        # case 4. ALPHA is on the right on parent 1 and
        #         ALPHA is on the left on parent 2
        #   -> Both corresponding locations are on the offspring 2
        #   -> Yield one between them, for some another alphabet,
        #      which assigned to both location on offspring 1

        # control case 3 and case 4
        # list of tuples: (alphabetid)
        off1_extra = [] # case 3. extra alphabets on offspring 1
        off2_extra = [] # case 4. extra alphabets on offspring 2

        for alphabet in abo:
            idx = get_index(alphabet)

            if idx in p1_left_pos_idx:
                if idx in p2_left_pos_idx:
                    new_pos1[idx] = pos1[idx]
                    new_pos2[idx] = pos2[idx]

                else:
                    # case 3
                    if off2_extra:
                        idx2 = off2_extra.pop(0)

                        if randint(0, 1):
                            new_pos1[idx] = pos1[idx]
                            new_pos2[idx] = pos1[idx2]
                            new_pos1[idx2] = pos2[idx]
                            new_pos2[idx2] = pos2[idx2]
                        else:
                            new_pos1[idx] = pos2[idx]
                            new_pos2[idx] = pos2[idx2]
                            new_pos1[idx2] = pos1[idx]
                            new_pos2[idx2] = pos1[idx2]

                    else:
                        off1_extra.append(idx)

            else:
                if idx not in p2_left_pos_idx:
                    new_pos1[idx] = pos2[idx]
                    new_pos2[idx] = pos1[idx]

                else:
                    # case 4
                    if off1_extra:
                        idx2 = off1_extra.pop(0)

                        if randint(0, 1):
                            new_pos1[idx] = pos2[idx2]
                            new_pos2[idx] = pos2[idx]
                            new_pos1[idx2] = pos1[idx2]
                            new_pos2[idx2] = pos1[idx]
                        else:
                            new_pos1[idx] = pos1[idx2]
                            new_pos2[idx] = pos1[idx]
                            new_pos1[idx2] = pos2[idx2]
                            new_pos2[idx2] = pos2[idx]

                    else:
                        off2_extra.append(idx)

        assert off1_extra == [] == off2_extra


        return new_pos1, new_pos2

    # Crossover method 4, BLX-alpha, (blend crossover)
    # http://www.tomaszgwiazda.com/blendX.htm
    def crossover4(pos1, pos2):
        assert len(pos1) == 26 == len(pos2)

        new_pos1 = np.zeros(pos1.shape)
        new_pos2 = np.zeros(pos2.shape)

        width, height = Solution.field.width, Solution.field.height
        dx = 4
        dy = 10

        for i in range(26):
            minx = max(min(pos1[i][0], pos2[i][0]) - dx, 0)
            maxx = min(max(pos1[i][0], pos2[i][0]) + dx, width)

            miny = max(min(pos1[i][1], pos2[i][1]) - dy, 0)
            maxy = min(max(pos1[i][1], pos2[i][1]) + dy, height)

            new_pos1[i] = [uniform(minx, maxx), uniform(miny, maxy)]
            new_pos2[i] = [uniform(minx, maxx), uniform(miny, maxy)]
        return new_pos1, new_pos2


    if True:
        new_pos1, new_pos2 = crossover3(sol1.positions, sol2.positions)

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

            if new_x <= 0:
                new_x = x
            elif new_x >= width:
                new_x = x

            if new_y <= 0:
                new_y = y
            elif new_y >= height:
                new_y = y

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
        
        # empty population for next generation
        next_population = []

        # add elite from current population
        next_population += GA_selection(current_population)

        if 'num_gen % 10 == 0':
            print(fitness(next_population[0]))
            #print('Gen : {} \t Fitness : {}'.format(num_gen,fitness(next_population[0])))
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