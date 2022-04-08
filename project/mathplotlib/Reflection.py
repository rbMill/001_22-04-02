import cmath
from matplotlib import pyplot as plt
import numpy as np

class PLTReflection(origin=[0.5,0.5],angle=90,bwidth=2,bheight=2):
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.iter_lim = 1000
        self.start()

    def start(self):
        for I in range(self.iter_lim):
            pass


