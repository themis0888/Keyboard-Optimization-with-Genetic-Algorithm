from solution import Solution
from config import CONFIG
import preprocess





# fitness function
def fitness(sol):
    fit_val = 0
    
    fit_val += 1.0 * fitness_area(sol) + fitness_dist(sol) + fitness_finger(sol)

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
def fitness_dist(sol, scale = 1):
    finger_list = sol.which_finger
    pos_list = sol.positions
    seq_freq = preprocess.seq_freq
    alp_freq = preprocess.alp_freq

    key_list = dict()
    for i in range(26):
        key_list[CONFIG['alphabet_string'][i]] = (finger_list[i], pos_list[i])
    fit_val = 0
    # pair is pair of alphabet such like 'aa'...
    for pair in seq_freq:

        # same key - fitness falue = 10
        if pair[0] == pair[1]:
            fit_val += 10 * seq_freq[pair] * scale

        # same finger but not same key - fitness falue = 10 to 20
        elif key_list[pair[0]][0] == key_list[pair[1]][0]:
            fit_val += (10 + abs(key_list[pair[0]][1][1] - key_list[pair[1]][1][1])/4) * seq_freq[pair] * scale

        # diff finger, same side hand - fit value = 5
        elif ((key_list[pair[0]][0] < 4) and (key_list[pair[1]][0] < 4) 
            or (key_list[pair[0]][0] >= 4) and (key_list[pair[1]][0] >= 4)):
            fit_val += 5 * seq_freq[pair] * scale

        # diff finger, diff side hand - fit value = 0

    return fit_val



def fitness_finger(sol, scale = 0.7):
    basecase_y = 20
    finger_list = sol.which_finger
    pos_list = sol.positions
    seq_freq = preprocess.seq_freq
    alp_freq = preprocess.alp_freq

    key_list = dict()
    for i in range(26):
        key_list[CONFIG['alphabet_string'][i]] = (finger_list[i], pos_list[i])
 
    fit_val = 0
    # give a penalty when the alphabet hitted by little finger
    # and when the key is far from initial position 
    for c in alp_freq:
        fit_val += scale * abs(basecase_y - key_list[c][1][1]) * alp_freq[c] / 20
        if key_list[c][0] == 0 or key_list[c][0] == 7:
            fit_val += scale * alp_freq[c]

    return fit_val



