import random
import types

import numpy as np
import math
from myLib.myLibrary import myList, myMath

from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'resizable', '1')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.lang.builder import Builder

from kivy.clock import Clock
from kivy.properties import StringProperty,NumericProperty,ListProperty,DictProperty,BoundedNumericProperty

from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from kivy.graphics import Color
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Bezier, Rectangle




class SnapGridLayout(Layout):
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

    # defining Elements
    # __anim_duration = 0.1
    # anim = None
    # mve = None
    # kivyArgs = {}
    # subArgs = {}
    # placement_mode = 'freeplace'
    # element_name = {}
    # elements = 0
    # col = 2
    # rows = 2
    # bwargs = {}
    # button_margin = [0, 0]
    # animate_motion = True
    # element_as_text = False
    # allow_do_layout = True
    # orientation = 'lr-bt'
    # placement_mode_pos = None
    # elements_pos = {}
    __anim_duration = NumericProperty(0.1)
    anim = None
    mve = None
    kivyArgs = {}
    subArgs = {}
    placement_mode = 'freeplace'
    element_name = DictProperty()
    elements = 0
    col = BoundedNumericProperty(1,min=1)
    rows = BoundedNumericProperty(1,min=1)
    bwargs = DictProperty()
    button_margin = [0, 0]
    animate_motion = True
    element_as_text = False
    allow_do_layout = True
    orientation = 'lr-bt'
    placement_mode_pos = None
    elements_pos = DictProperty()

    def __init__(self, **kwargs):
        super(SnapGridLayout, self).__init__(**self.kivyArgs)
        update = self._trigger_layout
        fbind = self.fbind
        fbind('spacing', update)
        fbind('padding', update)
        fbind('children', update)
        fbind('orientation', update)
        fbind('parent', update)
        fbind('size', update)
        fbind('pos', update)

        for k, v in kwargs.items():
            if k in dir(Layout):
                self.kivyArgs[k] = v
            else:
                self.subArgs[k] = v
                self.__setattr__(k, v)
        if type(self.elements) == list or type(self.elements) == list:
            numval = len(self.elements)
        elif type(self.elements) == dict or type(self.elements) == set:
            numval = len(self.elements)
        elif type(self.elements) == int:
            numval = self.elements
        else:
            raise TypeError('element type not valid, must be either list,int,dict,set,tuple')

        if numval > (self.rows * self.col):
            raise ValueError('element count exceed gridspace')
        self.dimensions = myList.gen2D(self.col, self.rows, orientation=self.orientation)
        self.dmx = [c / self.col for c in range(self.col)]
        self.dmy = [r / self.rows for r in range(self.rows)]
        bwargk = self.bwargs.keys()
        if 'size_hint' not in bwargk:
            self.bwargs['size_hint'] = [1, 1]
        if 'pos_hint' not in bwargk:
            self.bwargs['pos_hint'] = {'center_x': 0.5, 'center_y': 0.5}
        # binding events
        # generating elements
        if type(self.elements) == list or type(self.elements) == tuple:
            _lmn = self.elements
        elif type(self.elements) == int:
            _lmn = range(self.elements)
        else:
            _lmn = [0]

        def _1():
            elmlen = len(str(len(_lmn)))
            for i, D in zip(_lmn, self.dimensions):
                if type(i) != str:
                    i = '0' * (elmlen - len(str(i))) + str(i)
                button = Button(**self.bwargs)
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
                self.do_layout(animate=False)

            Clock.schedule_once(Clock.schedule_once(wb))
        Window.bind(on_resize=winbind)
        Clock.schedule_once(Clock.schedule_once(lambda *_: self.do_layout(animate=False)))


    def get_element(self, name, *args,**kwargs):
        res = self.element_name.get(name)
        if type(name) == int:
            res = self.children[name]
        return res

    def move(self, widg=None, *args,**kwargs):
        print('move',widg)
        if widg != None:
            if self.mve == None:
                def mv(*args):
                    widg.x = Window._mouse_x - int(widg.width / 2)
                    widg.y = Window.mouse_pos[1] - int(widg.height / 2)
                self.mve = Clock.schedule_interval(mv, 0.001)

    def release(self, widg=None, *args,**kwargs):
        print('release',widg)
        if widg != None:
            if self.mve != None:
                self.mve.cancel()
                self.mve = None
                def mv1(*args):
                    p_rt = self.elements_pos.get(widg)
                    cx = widg.x + int(widg.width / 2)
                    cy = widg.y + int(widg.height / 2)
                    px, py = cx / self.width, cy / self.height
                    xx = sorted(self.dmx.__add__([px]))
                    yy = sorted(self.dmy.__add__([py]))
                    x, y = xx[xx.index(px) - 1], yy[yy.index(py) - 1]
                    x, y = [myMath.clamp(x, 0, 1), myMath.clamp(y, 0, 1)]
                    rt = [x, y]
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
                            orien = self.placement_mode[11:16]
                            if occupant == None:
                                self.elements_pos[widg] = rt
                            else:
                                if self.placement_mode_pos == None:
                                    self.placement_mode_pos = myList.sort2D(self.dimensions, orien)
                                spm = self.placement_mode_pos
                                widgmet = {}
                                for i in spm[spm.index(rt):] + spm[:spm.index(rt)]:
                                    try:
                                        occup = list(self.elements_pos.keys())[
                                            list(self.elements_pos.values()).index(i)]
                                    except ValueError:
                                        occup = None
                                    widgmet[occup] = i
                                    if occup == None or occup == widg:
                                        break
                                tar = None
                                for w in list(widgmet.keys())[::-1]:
                                    p = widgmet.get(w)
                                    if w != None and tar != None and w != widg:
                                        self.elements_pos[w] = tar
                                    tar = p
                                self.elements_pos[widg] = rt
                mv1()
                self.do_layout()
            # Clock.schedule_once(self.do_layout)



    def do_layout(self, *args, **kwargs):
        if self.allow_do_layout:
            sW = self.width
            sH = self.height
            dx = (sW / self.col)
            dy = (sH / self.rows)
            ox, oy = 0, 0
            animate = kwargs.get('animate')
            ftime = False
            if animate == None:
                animate = self.animate_motion
            for k, v in self.elements_pos.items():
                xr, yr = v
                for i, d in k.pos_hint.items():
                    if i == 'center_x':
                        ox = -k.width / 2 + dx * d
                    elif i == 'left':
                        ox = dx * d
                    elif i == 'right':
                        ox = -k.width + dx * d
                    elif i == 'center_y':
                        oy = -k.height / 2 + dy * d
                    elif i == 'top':
                        oy = -k.height + dy * d
                    elif i == 'bottom':
                        oy = dy * d
                targ_pos = [xr * sW + ox, yr * sH + oy]
                kw, kh = k.size_hint
                if animate and not ftime:
                    size = {}
                    if kw != None:
                        size['width'] = kw * dx
                    if kh != None:
                        size['height'] = kh * dy
                    self.anim = Animation(pos=targ_pos, **size, duration=self.__anim_duration)
                    self.anim.start(k)
                elif not animate:
                    k.pos = targ_pos
                    if kw != None:
                        k.width = kw * dx
                    if kh != None:
                        k.height = kh * dy
            # super(do_layoutGridLayout, self).do_layout()

    def add_widget(self, widget, *args, **kwargs):
        self.elements_pos[widget] = self.dimensions[len(self.children)]
        widget.on_press=lambda :self.move(widget)
        widget.on_release=lambda :self.release(widget)
        super(SnapGridLayout, self).add_widget(widget,*args, **kwargs)

class Test(App):
    def build(self):
        self.title = 'GridLayoutTest'
        Window.maximize()
        lay = SnapGridLayout(elements=3, col=5, rows=5, element_as_text=True, orientation='tb-lr',
                             placement_mode='slideplace(tb-lr)'
                             , bwargs={'size_hint': [0.9, 0.9], 'pos_hint': {'center_x': 0.5, 'center_y': 0.5}})
        return lay


if __name__ == '__main__':
    Test().run()
