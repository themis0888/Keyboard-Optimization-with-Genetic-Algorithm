from solution import Solution
from config import CONFIG

# fitness function
def fitness(sol):
    fit_val = 0
    
    fit_val += 1.0 * fitness_area(sol)

    return fit_val

# auxiliary fitness functions

# area
def fitness_area(sol):
    avg_size = CONFIG['keyboard_width'] * CONFIG['keyboard_height'] / Solution.num_alphabet
    
    fit_val = 0

    for i in range(Solution.num_alphabet):
        A = sol.areas[i]
        Ar = sol.areas_rect[i]

        if A >= avg_size:
            if A / Ar >= 0.5:
                pass
            else:
                fit_val += (Ar - A) / Ar
        else:
            fit_val += (avg_size - A) / avg_size

    return fit_val
