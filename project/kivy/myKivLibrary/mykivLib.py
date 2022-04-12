import random
import numpy as np
import math

from myLib.myLibrary import myMath

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
        kivyArgs = {}
        subArgs = {}
        self.bwargs = {}
        self.col = 3
        self.elements = 1
        self.rows = 3
        self.element_as_text = False
        self.allow_snap = True
        for k,v in kwargs.items():
            if k in dir(Layout):
                kivyArgs[k] = v
            else:
                subArgs[k] = v
                self.__setattr__(k,v)

        super(SnapGrid, self).__init__(**kivyArgs)


        #defining Elements

        self.mve = None

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
            for i in _lmn:
                if type(i) != str:
                    i = '0' * (elmlen - len(str(i))) + str(i)
                button = Button(on_press=self.move,on_release=self.release,**self.bwargs)
                self.add_widget(button)
                if self.element_as_text:
                    button.text = i
                self.elements[i] = button

        _1()


    def move(self, widg):
        print(widg.pos,dir(widg))

        if self.mve == None:
            def mv(*args):
                widg.x = Window._mouse_x - int(widg.width / 2)
                widg.y = Window.mouse_pos[1] - int(widg.height / 2)
            self.mve = Clock.schedule_interval(mv, 0.000001)

    def snap(self):
        if self.allow_snap:
            pass
            # for i in self.children:
            #     relx = self.

    def release(self,widg):
        if self.mve != None:
            self.mve.cancel()
            self.mve = None
        self.snap()


class Test(App):
    def build(self):
        self.title = 'SnapGridTest'
        bwarg = {'text':'Yawa Ka Sir','size_hint':[None,None],'size':[200,200]}
        return SnapGrid(elements=3,cols=3,rows=3,orientation='lr-tb',bwargs=bwarg)
if __name__ == '__main__':
    Test().run()
