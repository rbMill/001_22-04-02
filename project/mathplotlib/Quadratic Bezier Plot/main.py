from matplotlib import pyplot as plt
import numpy as np


if False | False:
    print('yee?')
class Bezier:
    def __init__(self):
        fig, self.ax = plt.subplots()
        self.show_control = True
        self.show_procedure = True


    def myBezier(self,p1=None,p2=None,p3=None):
        if p1 == None or p2 == None or p3 == None:
            px,py = [0,0,1],[0,1,1]
        else:
            px,py = [p1[0],p2[0],p3[0]],[p1[1],p2[1],p3[1]]


        ofst = 0.2
        xlim = [0-ofst,1+ofst]
        ylim = [0-ofst,1+ofst]
        res = 50

        trajx = np.linspace(px[0],px[1],res)
        trajy = np.linspace(py[0],py[1],res)

        trajx1 = np.linspace(px[1],px[2],res)
        trajy1 = np.linspace(py[1],py[2],res)

        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_aspect('equal')

        # plotting
        if self.show_control:
            self.ax.plot(px,py,'Black')

        _x,_y = px[0],py[0]
        _x1,_y1 = px[1],py[1]


        nx,ny = _x,_y

        for i,(x,y,x1,y1) in enumerate(zip(trajx,trajy,trajx1,trajy1)):
            if self.show_procedure:
                self.ax.plot([_x,x],[_y,y],'red')
                self.ax.plot([_x1,x1],[_y1,y1],'blue')

            _x,_y = x,y
            _x1, _y1 = x1, y1

            prc = i/res
            dx = x + (x1-x)*prc
            dy = y + (y1-y)*prc
            self.ax.plot([nx, dx], [ny, dy], 'green')
            nx,ny = dx, dy

            plt.pause(0.001)

bz = Bezier()
bz.show_control = False
bz.show_procedure = False

bz.myBezier([1,1],[1,0],[0,0]) #

bz.myBezier([0,0],[0,0.5],[0.5,0.5])

bz.myBezier([1,1],[0,1],[0,0]) #

bz.myBezier([0,0],[0.5,0],[0.5,0.5])

bz.myBezier([0,1],[0,0],[1,0]) #

bz.myBezier([1,0],[1,0.5],[0.5,0.5])

bz.myBezier([0,1],[0,0],[1,0]) #

bz.myBezier([1,0],[0.5,0],[0.5,0.5])

bz.myBezier([0,1],[1,1],[1,0]) #


plt.show()