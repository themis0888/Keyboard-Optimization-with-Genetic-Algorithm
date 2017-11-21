from field import Field
from config import CONFIG

# individual
class Solution:
    # data structure : list of tuples
    # [(x, y), --> alphabet a (index = 0) and x, y are floats
    #  (x, y), --> alphabet b (index = 1)
    #  .
    #  .
    #  .
    #  (x, y), --> alphabet z (index = 25)
    #  (x, y)  --> space bar
    # ]

    num_alphabet = 26

    field = Field()

    # constructor
    def __init__(self, seed=None):
        # generate solution with seed list
        if seed:
            self.positions = seed
        # generate random solution
        else:
            # random generate ...
            pass

    # get coordinate of key by name
    def get_loc_by_name(self, keyname):
        # for space bar
        if keyname == 'space':
            return self.positions[Solution.num_alphabet]
        # for a to z
        else:
            return self.positions[ord(keyname) - 97]

    # get coordinate of key
    def get_loc(self, index):
        return self.positions[index]

    # get which finger will push the key (0 ~ 9)
    def which_finger(self):
        # finger_number : which finger will push the key
        # move_distance : how much distance finger have to move to push the key
        # ...
        finger_number = 0
        move_distance = 0
        return finger_number, move_distance

    # plot voronoi diagram
    def plot():
        pass

#sol = Solution([(i, i) for i in range(27)])
