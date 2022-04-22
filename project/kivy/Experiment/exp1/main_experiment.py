from myLib.myKivLibrary.snapgridlayout import SnapGridLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.base import Builder




class uilayout(BoxLayout):
    def __init__(self,**kwargs):
        super(uilayout, self).__init__(**kwargs)

class editor(SnapGridLayout):
    def __init__(self,**kwargs):
        # # other = {'elements':0,'placement_mode':'stackplace','col':4,'rows':2,'bwargs' : {'size_hint':[1,1]}}
        # # kwargs.update(other)
        # print('called')
        super(editor, self).__init__(**kwargs)
        self.orientation = 'bt-lr'
        self.col = 3
        self.rows = 2
        self.add_widget(Button(**self.bwargs))

class APPname(App):
    def build(self):
        Builder.load_file('main_experiment.kv')
        self.title == 'experiment'
        return uilayout()

if __name__ == '__main__':
    Window.maximize()
    APPname().run()
