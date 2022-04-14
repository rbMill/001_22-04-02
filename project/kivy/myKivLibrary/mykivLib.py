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
            col: int, number of columns of the layout/grid
            rows: int, number of rows of the layout/grid
            placement_mode, str, 
                'freeplace' - placing only when a greed is free
                'switchplace' - placing anywere and element will switch place
                'stackplace' - placing on an element stacks on top of it
                'slidespace(direction)' - placing an element unfreely pushes neighboring widget
                    direction uses lr-bt,lr-tb,bt-lr...etc to describe cascading repositioning direction 
        '''


    def __init__(self,**kwargs):
        #defining Elements

        self.mve = None
        kivyArgs = {}
        subArgs = {}
        self.placement_mode = 'freeplace'
        self.element_name = {}
        self.col = 3
        self.elements = 1
        self.rows = 3
        self.bwargs = {}
        self.button_margin = [0,0]
        self.element_as_text = False
        self.allow_snap = True
        self.orientation = 'lr-bt'
        self.elements_pos = {}

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
            self.bwargs['size_hint'] = [1,1]

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
            elmlen = len(str(len(_lmn)))
            for i,D in zip(_lmn,self.dimensions):
                if type(i) != str:
                    i = '0' * (elmlen - len(str(i))) + str(i)
                button = Button(on_press=self.move,on_release=self.release,**self.bwargs)
                self.add_widget(button)
                if self.element_as_text:
                    button.text = i
                self.elements_pos[button] = D
                self.element_name[i] = button
        _1()
        Window.bind(on_resize=lambda *args: Clock.schedule_once(Clock.schedule_once(self.snap)))
        Clock.schedule_once(Clock.schedule_once(self.snap))

    def move(self, widg):
        if self.mve == None:
            def mv(*args):
                widg.x = Window._mouse_x - int(widg.width / 2)
                widg.y = Window.mouse_pos[1] - int(widg.height / 2)
            self.mve = Clock.schedule_interval(mv, 0.000001)


    def get_element(self,name,*args):
        res = self.element_name.get(name)
        if type(name) == int:
            res = self.children[name]
        return res

    def do_layout(self, *largs):
        pass

    def release(self,widg):
        if self.mve != None:
            self.mve.cancel()
            self.mve = None
            def mv1(*args):
                p_rt = self.elements_pos.get(widg)
                cx = widg.x + int(widg.width / 2)
                cy = widg.y + int(widg.height / 2)
                px,py = cx/self.width,cy/self.height
                xx = sorted(self.dmx.__add__([px]))
                yy = sorted(self.dmy.__add__([py]))
                x,y = xx[xx.index(px)-1],yy[yy.index(py)-1]
                rt = [myMath.clamp(x,0,1),myMath.clamp(y,0,1)]
                try:
                    occupant = list(self.elements_pos.keys())[list(self.elements_pos.values()).index(rt)]
                except ValueError:
                    occupant = None
                if p_rt != rt:
                    if self.placement_mode == 'stackplace':
                        self.elements_pos[widg] = rt
                    elif self.placement_mode == 'freeplace' and occupant == None:
                        self.elements_pos[widg] = rt
                    elif self.placement_mode == 'switchplace':
                        if occupant == None:
                            self.elements_pos[widg] = rt
                        else:
                            self.elements_pos[occupant] = p_rt
                            self.elements_pos[widg] = rt

            mv1()
            self.snap()

    def snap(self,*args):
        if self.allow_snap:
            dx = (self.width / self.col)
            dy = (self.height / self.rows)
            ox,oy = 0,0
            for k,v in self.elements_pos.items():
                xr,yr = v
                for i,d in k.pos_hint.items():
                    if i == 'center_x':
                        ox = -k.width/2 + dx * d
                    elif i == 'left':
                        ox = dx * d
                    elif i == 'right':
                        ox = -k.width + dx * d
                    elif i == 'center_y':
                        oy = -k.height/2 + dy * d
                    elif i == 'top':
                        oy = -k.height + dy * d
                    elif i == 'bottom':
                        oy = dy * d

                k.pos = [xr*self.width+ox,yr*self.height+oy]
                kw, kh = k.size_hint
                if kw != None:
                    k.width = kw*dx
                if kh != None:
                    k.height = kh*dy


class Test(App):
    def build(self):
        self.title = 'SnapGridTest'
        bwarg = {'size_hint':[1,1],'pos_hint':{'center_x':0.5,'center_y':0.5}}
        Window.maximize()
        lay = SnapGrid(elements=7,col=2,rows=4,orientation='tb-lr',placement_mode='switchplace',element_as_text=True,bwargs=bwarg)
        return lay

if __name__ == '__main__':
    Test().run()
