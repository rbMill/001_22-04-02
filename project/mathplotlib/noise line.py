import cmath
import random
import numpy as np

from matplotlib import pyplot as plt


x_,y_ = -1,0
fig, ax = plt.subplots()
a = 2

xlim = [-3,3]
ylim = [-3,3]

c = 4/3

ax.set_aspect('equal')
px = 0.5
py = 0.5
for i in range(1000):

    plt.pause(0.0001)

plt.show()