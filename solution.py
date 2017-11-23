from field import Field
from config import CONFIG
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# individual
class Solution:
    # data structure : numpy 2D array
    # [[x, y], --> alphabet a (index = 0) and x, y are floats
    #  [x, y], --> alphabet b (index = 1)
    #  .
    #  .
    #  .
    #  [x, y], --> alphabet z (index = 25)
    #  [x, y]  --> space bar
    # ]

    num_alphabet = 26

    field = Field()

    # constructor
    def __init__(self, seed=None):
        # generate solution with seed list
        if seed:
            self.positions = np.array(seed)
        # generate random solution
        else:
            # random generate
            self.positions = np.array([[np.random.rand() * CONFIG['keyboard_width'], np.random.rand() * CONFIG['keyboard_height']] for i in range(27)])

    # get coordinate of key by name
    # ex)
    #   sol.get_loc_by_name('a')
    #   sol.get_loc_by_name('space')
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
    def plot(self):
        # labels for labeling points
        labels = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','SPACE']

        # compute Voronoi tesselation
        vor = Voronoi(self.positions)

        # plot
        voronoi_plot_2d(vor, show_vertices=False, show_points=False)

        # draw points and labels
        plt.scatter(self.positions[:, 0], self.positions[:, 1], s=10)
        for i, txt in enumerate(labels):
            plt.annotate(txt, (self.positions[:, 0][i], self.positions[:, 1][i]))

        # config plt
        plt.xlim(0, CONFIG['keyboard_width'])
        plt.ylim(0, CONFIG['keyboard_height'])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    # calculate area of each voronoi cells
    def area(self):
        # calculate area of polygon using showlace formula
        def poly_area(x,y):
            return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

        # expand voronoi diagram for 4-directions
        under = self.positions * np.array([1, -1])
        right = self.positions * np.array([-1, 1]) + np.array([2 * CONFIG['keyboard_width'], 0])
        upper = self.positions * np.array([1, -1]) + np.array([0, 2 * CONFIG['keyboard_height']])
        left = self.positions * np.array([-1, 1])

        points = np.concatenate((self.positions, under, right, upper, left), axis=0)

        # make voronoi diagram
        vor = Voronoi(points)

        # list of areas of each voronoi cells
        areas = []

        # for each cells from a to spacebar, calculate area of cells
        for i in range(Solution.num_alphabet + 1):
            index_region = vor.point_region[i]
            index_vertices = vor.regions[index_region]

            # coordinate of each vertices
            x_coord = []
            y_coord = []

            for j in index_vertices:
                x_coord.append(vor.vertices[j][0])
                y_coord.append(vor.vertices[j][1])

            areas.append(poly_area(x_coord, y_coord))
        
        return areas
