import random
import numpy as np
import math
from myLib.myLibrary import myList,myMath

from kivy.app import App
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.config import Config
from kivy.graphics.vertex_instructions import Bezier, Rectangle

Config.set('graphics', 'resizable', '1')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.lang.builder import Builder
from kivy.clock import Clock


class SnapGrid(Layout):
    __doc__ = \
        '''
        Params:
            elements: int or list; the number of generated buttons or a list with a correspondng name
        '''


    def __init__(self,**kwargs):
        #defining Elements

        self.mve = None
        kivyArgs = {}
        subArgs = {}
        self.__element_name = {}
        self.col = 3
        self.elements = 1
        self.rows = 3
        self.bwargs = {}
        self.button_margin = [0,0]
        self.element_as_text = False
        self.allow_snap = True
        self.orientation = 'lr-bt'

        for k,v in kwargs.items():
            if k in dir(Layout):
                kivyArgs[k] = v
            else:
                subArgs[k] = v
                self.__setattr__(k,v)
        if self.elements > (self.rows*self.col):
            raise ValueError('element count exceed gridspace')
        self.dimensions = myList.gen2D(self.col,self.rows,orientation=self.orientation)
        self.dmx = [c/self.col for c in range(self.col) ]
        self.dmy = [r / self.rows for r in range(self.rows)]
        if 'size_hint' not in self.bwargs.keys():
            self.bwargs['size_hint'] = [1/self.col,1/self.rows]

        #binding events
        super(SnapGrid, self).__init__(**kivyArgs)
        #generating elements
        if type(self.elements) == list or type(self.elements) == tuple:
            _lmn = self.elements
        elif type(self.elements) == int:
            _lmn = range(self.elements)
        else:
            _lmn = [0]
        def _1():
            self.elements = {}
            elmlen = len(str(len(_lmn)))
            for i,D in zip(_lmn,self.dimensions):
                if type(i) != str:
                    i = '0' * (elmlen - len(str(i))) + str(i)
                button = Button(on_press=self.move,on_release=self.release,**self.bwargs)
                self.add_widget(button)
                if self.element_as_text:
                    button.text = i
                self.elements[button] = D
                self.__element_name[i] = button
        _1()
        Window.bind(on_resize=lambda *args: Clock.schedule_once(self.snap))
        Clock.schedule_once(self.snap)

    def move(self, widg):
        if self.mve == None:
            def mv(*args):
                widg.x = Window._mouse_x - int(widg.width / 2)
                widg.y = Window.mouse_pos[1] - int(widg.height / 2)
            self.mve = Clock.schedule_interval(mv, 0.000001)


    def get_element(self,name,*args):
        return self.__element_name.get(name)

    def do_layout(self, *largs):
        pass

    def release(self,widg):
        if self.mve != None:
            self.mve.cancel()
            self.mve = None
            def mv1(*args):
                cx = widg.x + int(widg.width / 2)
                cy = widg.y + int(widg.height / 2)
                px,py = cx/self.width,cy/self.height
                xx = sorted(self.dmx.__add__([px]))
                yy = sorted(self.dmy.__add__([py]))
                x,y = xx[xx.index(px)-1],yy[yy.index(py)-1]
                rt = [myMath.clamp(x,0,1),myMath.clamp(y,0,1)]
                self.elements[widg] = rt
            mv1()
            self.snap()

    def snap(self,*args):
        if self.allow_snap:
            dx = (self.height / self.rows)
            dy = (self.height / self.rows)
            ax = self.button_margin[0] * dx
            ay = self.button_margin[1] * dy
            for k,v in self.elements.items():
                xr,yr = v
                kw,kh = k.size_hint
                ox = ax
                oy = ay
                print(ox,oy)
                k.pos = [xr*self.width+ox,yr*self.height+oy]
                if kw != None:
                    k.width = kw*self.width
                if kh != None:
                    k.height = kh*self.height


class Test(App):
    def build(self):
        self.title = 'SnapGridTest'
        bwarg = {'size_hint':[0.2,0.2]}
        Window.maximize()
        lay = SnapGrid(elements=16,col=4,rows=4,orientation='bt-lr',element_as_text=True,bwargs=bwarg
                       ,button_margin=[0.5,0.5])
        return lay

if __name__ == '__main__':
    Test().run()
