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
trajx = []
trajy = []
for i in range(360*5):
    ax.clear()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    I = i
    # r = random.randint(9,11)/10

    i = ((i) * cmath.pi)/180

    r = cmath.sin(i*4)
    x1 = cmath.cos(i**1.1)
    x2 = cmath.cos(i**0.5) + x1

    y1 = cmath.sin(i**1.1)
    y2 = cmath.sin(i**0.5) + y1

    xs = [0,x1,x2]
    ys = [0,y1,y2]

    trajx.append(xs[-1])
    trajy.append(ys[-1])
    ax.plot(trajx, trajy, 'red')
    ax.plot(xs,ys,'black')

    plt.pause(0.0001)

plt.show()