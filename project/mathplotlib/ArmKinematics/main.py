from matplotlib import pyplot as plt
import numpy as np
import math

x,y = [],[]
fig, ax = plt.subplots()
a = 2
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
for i in range(360*1):
    i = i*math.pi/180
    x.append(math.cos(i)*i/360)
    y.append(math.sin(i)*i/360)
    if len(x) >= 22:
        x = x[-22:]
    if len(y) >= 22:
        y = y[-22:]
    ax.plot(x, y,'black')
    plt.pause(0.001)
ax.set_aspect('equal')

plt.show()