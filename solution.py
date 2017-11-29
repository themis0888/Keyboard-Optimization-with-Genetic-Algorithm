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
    # ]

    num_alphabet = 26

    field = Field()

    # constructor
    def __init__(self, seed=None):
        # generate solution with seed list
        if seed is not None:
            self.positions = np.array(seed)
        # generate random solution
        else:
            # auxiliary random function which never returns 0
            def rand_nonzero():
                temp = np.random.rand()
                while temp == 0.0:
                    temp = np.random.rand()
                return temp

            # random generate
            self.positions = np.array([[rand_nonzero() * CONFIG['keyboard_width'], rand_nonzero() * CONFIG['keyboard_height']] for i in range(Solution.num_alphabet)])

        # calculate necessary values

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

        # list of rectangular areas of each voronoi cells
        areas_rect = []

        # list of central points of each voronoi cells
        central_points = []

        # list of number of fingers correponding to alphabets
        which_finger = []

        # list of coordinates of vertices of each voronoi regions
        voronoi_edges = []

        # for each cells from a to spacebar, calculate area of cells
        for i in range(Solution.num_alphabet):
            index_region = vor.point_region[i]
            index_vertices = vor.regions[index_region]

            # coordinate of each vertices
            x_coord = []
            y_coord = []

            # calculate areas
            for j in index_vertices:
                x_coord.append(vor.vertices[j][0])
                y_coord.append(vor.vertices[j][1])

            areas.append(poly_area(x_coord, y_coord))

            # calculate vertices of voronoi region
            edge_vertices = []
            for j in index_vertices:
                edge_vertices.append(vor.vertices[j])
            voronoi_edges.append(edge_vertices)

            # calculate min and max of x, y coord
            min_x = min(x_coord)
            max_x = max(x_coord)
            min_y = min(y_coord)
            max_y = max(y_coord)

            # calculate rectangular areas
            rect_width = abs(max_x - min_x)
            rect_height = abs(max_y - min_y)

            areas_rect.append(rect_width * rect_height)

            # calculate central point of each voronoi cells
            cent_x = (min_x + max_x) / 2
            cent_y = (min_y + max_y) / 2

            central_points.append([cent_x, cent_y])

            # calculate which finger will push the key
            which_finger.append(Solution.field.which_finger([cent_x, cent_y]))
        
        # add attributes
        self.areas = areas
        self.areas_rect = areas_rect
        self.central_points = central_points
        self.which_finger = which_finger
        self.voronoi_edges = voronoi_edges

        self.vor = vor

    # get coordinate of key by name
    # ex)
    #   sol.get_loc_by_name('a')
    def get_loc_by_name(self, keyname):
        return self.positions[ord(keyname) - 97]

    # get coordinate of key
    def get_loc(self, index):
        return self.positions[index]

    # plot voronoi diagram
    def plot(self):
        # labels for labeling points
        labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # plot
        voronoi_plot_2d(self.vor, show_vertices=False, show_points=False)

        colors = ['#ffb3b3', '#ffd9b3', '#ffffb3', '#d9ffb3', '#b3ffff', '#b3d9ff', '#b3b3ff', '#d9b3ff']
        for i in range(Solution.num_alphabet):
            index_region = self.vor.point_region[i]
            index_vertices = self.vor.regions[index_region]
            polygon = [self.vor.vertices[j] for j in index_vertices]
            plt.fill(*zip(*polygon), colors[self.which_finger[i]])

        # draw points and labels
        plt.scatter(self.positions[:, 0], self.positions[:, 1], s=10, zorder=100)
        for i, txt in enumerate(labels):
            plt.annotate(txt, (self.positions[:, 0][i], self.positions[:, 1][i]))

        # config plt
        plt.xlim(0, CONFIG['keyboard_width'])
        plt.ylim(0, CONFIG['keyboard_height'])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
