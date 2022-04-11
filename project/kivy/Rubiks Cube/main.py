import random
import numpy as np

from myLib.myLibrary import myMath

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.config import Config
from kivy.graphics.vertex_instructions import Bezier,Rectangle
Config.set('graphics','resizable','1')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.lang.builder import Builder
from kivy.clock import Clock

class rubiksUI(AnchorLayout):
	def __init__(self, **kwargs):
		super(rubiksUI, self).__init__(**kwargs)


class grpRubiks(Button):
	def __init__(self, **kwargs):
		super(grpRubiks, self).__init__(**kwargs)
		self.rec = None
		self.col = None
		self.size = [600,600]
		Window.bind(on_resize=self.fixAxpect)
		_x,_y = [100,100,400],[100,400,100]

	def fixAxpect(self,*args):
		if self.rec != None and self.col != None:
			self.col.a = 0.5
			def _(*args):
				self.rec.pos = self.pos
				self.rec.size = self.size
				self.col.a = 1
			Clock.schedule_once(_)

	def _init1(self,*args):
		r = random.randint
		self.canvas.before.clear()
		_points = []
		# for i in range(30):
        #     ofs = 0
        #     val = int(random.random()*(self.width*self.height)**0.5) + of
		# 	# val = myMath.clamp(val,self.x,self.width)
		# 	# _points.append(val)
		# with self.canvas.before:
		# 	self.col = Color(r(0,100)/100,r(0,100)/100,r(0,100)/100,1)
		# 	self.rec = Rectangle(pos=self.pos,size=self.size)
		# 	self.col = Color(r(0, 100) / 100, r(0, 100) / 100, r(0, 100) / 100, 1)
		# 	self.bez = Bezier(points=_points,segments=300)
		# print(self.bez.points)

	def func(self,*args):
		print(self.children)

class Rubiks(App):
	def Build(self):
		self.title = 'Rubiks'
		Builder.load_file('rubiks.kv')
		return rubiksUI()



Window.size = Window.size
Window.maximize()
Window.clearcolor = [0.2,0.2,0.22,1]
Rubiks().run()