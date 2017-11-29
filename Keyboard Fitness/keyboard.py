from field import Field
from config import CONFIG
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

x_len = CONFIG['keyboard_width']
y_len = CONFIG['keyboard_height']


temp = []
string = 'qwertyuiop'
for i in range(len(string)):
    temp.append((string[i], [i * x_len / 10 + x_len/20, y_len * 5 / 6]))
string = '!asdfghjkl@'
for i in range(len(string)):
    temp.append((string[i], [i * x_len / 10, y_len * 3 / 6]))
string = '#zxcvbnm$%^'
for i in range(len(string)):
    temp.append((string[i], [i * x_len / 10 + x_len/20, y_len * 1 / 6]))


alp_array = []
for i in temp:

    alp_array.append(i[1])


