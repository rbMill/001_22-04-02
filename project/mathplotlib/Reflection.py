import cmath
from matplotlib import pyplot as plt
import numpy as np

class PLTReflection:
    def __init__(self,origin=[0,0],angle=45,bwidth=1,bheight=1):
        self.origin = origin
        self.a = angle
        self.xlen = bwidth
        self.ylen = bheight
        bw = bwidth/2
        bh = bheight/2
        if origin[0] < -bw or origin[0] > bw or origin[1] < -bw or origin[1] > bh:
            raise ValueError('origin not within bounding box')
        self.xlim = [-bw*1.5,bw*1.5]
        self.ylim = [-bh*1.5,bh*1.5]
        self.fig, self.ax = plt.subplots()
        self.iter_lim = 10
        self.fixAx()
        _x,_y = [-bw,-bw,bw,bw,-bw],[bh,-bh,-bh,bh,bh]
        self.ax.plot([origin[0],origin[0]+0.1],[origin[1],origin[1]+0.1], 'blue')
        self.ax.plot(_x,_y,'blue')
        self.start()

    def fixAx(self):
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        self.ax.set_aspect('equal')

    def start(self):
        xp,yp = self.origin
        xval = np.array([xp],dtype='float')
        yval = np.array([yp],dtype='float')
        xv = [xp]
        yv = [yp]
        a = self.a
        for I in range(self.iter_lim):
            an = (a + I*90)*cmath.pi/180
            if 0 <= a <= 90:
                h1 = (1-xp)/cmath.cos(self.a)
                h2 = (1-yp)/cmath.sin(self.a)
            # xf =
            # yf =
            mx = cmath.cos(an)+xp
            my = cmath.sin(an)+yp
            xv.append(mx)
            yv.append(my)
            plt.pause(0.1)
            self.ax.plot(xv,yv,'red')
        print(xv,yv)
        plt.show()

PLTReflection()
