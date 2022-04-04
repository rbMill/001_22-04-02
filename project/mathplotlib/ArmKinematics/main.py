from matplotlib import pyplot as plt
import math

x,y = [],[]
for i in range(360):
    x.append(math.cos(i))
    y.append(math.sin(i))

plt.plot(x,y)
plt.show()