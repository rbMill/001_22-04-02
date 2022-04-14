import random
import numpy as np
import math
from myLib.myLibrary import myList,myMath

from kivy.app import App
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.animation import Animation
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
            elements: int,list,dict;
                int: Generates the number of elements with prefab
                list: Generates the number of elements with prefab and intterator name_value
            col: int, number of columns of the layout/grid
            rows: int, number of rows of the layout/grid
            placement_mode, str, 
                'freeplace' - placing only when a greed is free
                'switchplace' - placing anywere and element will switch place
                'stackplace' - placing on an element stacks on top of it
                'slidesplace(direction)' - placing an element unfreely pushes neighboring widget
                    direction uses lr-bt,lr-tb,bt-lr...etc to describe cascading repositioning direction 
            element_as_text: bool, the widget will display text by their generated/stored identifier
            
            bwarg
        '''


    def __init__(self,**kwargs):
        #defining Elements
        self.__anim_duration = 0.1
        self.anim = None
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
        self.animate_motion = True
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
        if type(self.elements) == list or type(self.elements) == list:
            numval = len(self.elements)
        elif type(self.elements) == dict or type(self.elements) == set:
            numval = len(self.elements)
        elif type(self.elements) == int:
            numval = self.elements
        else:
            raise TypeError('element type not valid, must be either list,int,dict,set,tuple')

        if numval > (self.rows*self.col):
            raise ValueError('element count exceed gridspace')
        self.dimensions = myList.gen2D(self.col,self.rows,orientation=self.orientation)
        self.dmx = [c/self.col for c in range(self.col) ]
        self.dmy = [r / self.rows for r in range(self.rows)]
        bwargk = self.bwargs.keys()
        if 'size_hint' not in bwargk:
            self.bwargs['size_hint'] = [1,1]
        if 'pos_hint' not in bwargk:
            self.bwargs['pos_hint'] = {'center_x':0.5,'center_y':0.5}
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
                if i in self.element_name.keys():
                    raise Warning('a widget with an identifier already exist,\nwhich will result to lost of reference')
                self.element_name[i] = button
        _1()
        def winbind(*_):
            def wb(*_):
                for i in self.children:
                    Animation.stop_all(i)
                self.snap(animate=False)
            Clock.schedule_once(Clock.schedule_once(wb))
        Window.bind(on_resize=winbind)
        Clock.schedule_once(Clock.schedule_once(lambda *_:self.snap(animate=False)))

    def move(self, widg,**kwargs):
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
        return

    def release(self,widg,**kwargs):
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
                x, y = xx[xx.index(px) - 1], yy[yy.index(py) - 1]
                x,y = [myMath.clamp(x,0,1),myMath.clamp(y,0,1)]
                rt = [x,y]
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
                    elif self.placement_mode[:10] == 'slideplace':
                        print(self.placement_mode[10:17])
            mv1()
            self.snap()

    def snap(self,*args,**kwargs):
        if self.allow_snap:
            sW = self.width
            sH = self.height
            dx = (sW / self.col)
            dy = (sH / self.rows)
            ox,oy = 0,0
            animate = kwargs.get('animate')
            ftime = False
            if animate == None:
                animate = self.animate_motion
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
                targ_pos = [xr*sW+ox,yr*sH+oy]
                kw, kh = k.size_hint
                if animate and not ftime:
                    size = {}
                    if kw != None:
                        size['width'] = kw*dx
                    if kh != None:
                        size['height'] = kh*dy
                    self.anim = Animation(pos=targ_pos,**size,duration=self.__anim_duration)
                    self.anim.start(k)
                elif not animate:
                    k.pos = targ_pos
                    if kw != None:
                        k.width = kw*dx
                    if kh != None:
                        k.height = kh*dy


class Test(App):
    def build(self):
        self.title = 'SnapGridTest'
        Window.maximize()
        lay = SnapGrid(elements=4,placement_mode='slideplace(lr-bt)')
        return lay

if __name__ == '__main__':
    Test().run()
