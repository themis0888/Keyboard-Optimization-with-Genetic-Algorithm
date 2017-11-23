from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import math
import random

num_key = 27
x_range = 10
y_range = 4
points = []
for i in range(num_key):
	points.append((random.randrange(0,x_range), random.randrange(0,y_range)))
vor = Voronoi(points)

voronoi_plot_2d(vor)
plt.show()