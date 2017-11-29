# configuration file
CONFIG = {
    'keyboard_width': 100,
    'keyboard_height': 32,

    'GA_num_generation': 200,
    'GA_num_population': 100,
    'GA_num_selection': 20,

    'GA_mutation_rate': 0.1,
    'GA_mutation_noise': 5,
    'GA_mutation_swap_rate': 0.6,
    'GA_mutation_swap_limit': 40,

    # https://en.wikipedia.org/wiki/Letter_frequency 
    'letter_frequency': "etaonrishdlfcmugypwbvkjxqz",

    'alphabet_string': 'abcdefghijklmnopqrstuvwxyz',
    #'key_string' : 'qwertyuiop!asdfghjkl@#zxcvbnm$%^',
    #3rd style korean keyboard
    #'key_string' : 'vxuoj@@@cv@@@lkm@d@wqx@@@phn@g@@',
    #'key2_string' : '@@ecO@@@@@@@@gv@@@@@@@z@@ew@@@@z',
    # Dvorak
    'key_string' : '@@@pyfgcrl@aoeuidhtns@@qjkxbmwvz',
    'finger_list' : [0,1,2,3,3,4,4,5,6,7,0,0,1,2,3,3,4,4,5,6,7,0,0,1,2,3,3,4,4,5,5,6],
}
