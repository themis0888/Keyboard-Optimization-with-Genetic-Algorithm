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


# distance 
def fitness_dist(sol):
    char_freq, seq_freq = preprocess()

    finger_list = sol.which_finger
    pos_list = sol.positions
    key_list = dict()
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    for i in range(26):
        key_list[alphabet[i]] = (finger_list[i], pos_list[i])

    fit_val = 0
    # pair is pair of alphabet such like 'aa'...
    for pair in seq_freq:

        # same key - fitness falue = 1 
        if pair[0] == pair[1]:
            fit_val += 1

        # same finger but not same key - fitness falue = 1.5
        elif key_list[pair[0]] == key_list[pair[1]]:
            fit_val += 1.5

        # diff finger, same side hand - fit value = 0.5
        elif ((key_list[pair[0]] < 4) and (key_list[pair[1]] < 4) 
            or (key_list[pair[0]] >= 4) and (key_list[pair[1]] >= 4)):
            fit_val += 0.5

        # diff finger, diff side hand - fit value = 0


    return fit_val