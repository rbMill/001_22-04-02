from matplotlib import pyplot as plt
import numpy as np
import math

x,y = [],[]
for i in range(360*1):
        x.append(math.cos(i*math.pi/180)*math.sin(i/math.pi))
        y.append(math.sin(i*math.pi/180)*math.cos(i/math.pi))


fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_aspect('equal')
plt.show()