from matplotlib import pyplot as plt
import numpy as np


fig, ax = plt.subplots()

a = 2

ofst = 0.2

xlim = [0-ofst,1+ofst]
ylim = [0-ofst,1+ofst]

c = 4/3

px,py = [0,0,1],[0,1,1]

res = 50

trajx = np.linspace(px[0],px[1],res)
trajy = np.linspace(py[0],py[1],res)

trajx1 = np.linspace(px[1],px[2],res)
trajy1 = np.linspace(py[1],py[2],res)

ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_aspect('equal')

# plotting
ax.plot(px,py,'Black')

_x,_y = px[0],py[0]
_x1,_y1 = px[1],py[1]


nx,ny = _x,_y

for i,(x,y,x1,y1) in enumerate(zip(trajx,trajy,trajx1,trajy1)):
    ax.plot([_x,x],[_y,y],'red')
    _x,_y = x,y

    ax.plot([_x1,x1],[_y1,y1],'blue')
    _x1, _y1 = x1, y1

    prc = i/res
    dx = x + (x1-x)*prc
    dy = y + (y1-y)*prc
    ax.plot([nx, dx], [ny, dy], 'green')
    nx,ny = dx, dy

    plt.pause(0.001)
plt.show()