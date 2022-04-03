from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics','resizable','1')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.lang.builder import Builder
from kivy.clock import Clock

class UI(AnchorLayout):
    def __init__(self,**kwargs):
        super(UI, self).__init__(**kwargs)
        self.mouseEvent = None
        self.kBoard = Window.request_keyboard(self.kBoard_on_close,self,'text')
        self.kBoard.bind(on_key_down=self.kBoard_on_use,on_key_up=self.kBoard_on_use)
    def kBoard_on_use(self,kb=None,key=None,text=None,modifiers=None):
        args = (kb,key,text,modifiers)
        if key[1] == 'spacebar':
            print('space')
    def kBoard_not_use(self):
        pass

    def on_motion



    def kBoard_on_close(self):
        self.kBoard.unbind

    def on_CLD(self,widg,parent=None):
        if self.mouseEvent == None:
            if parent == None:
                parent = widg.parent
            def on_hold_m(args):
                Mpos = Window.mouse_pos
                d_x,d_y = round((Mpos[0]-parent.x)/(parent.width),3),round((Mpos[1]-parent.y)/(parent.height),3)
                widg.text = str([d_x,d_y]) + str(Mpos)
            self.mouseEvent = Clock.schedule_interval(on_hold_m,0.001)
        else:
            self.off_CLD()

    def off_CLD(self,*args):
        if self.mouseEvent != None:
            self.mouseEvent.cancel()
            print('canceling....')
            self.mouseEvent = None

class SIS_maker(App):
    def Build(self):
        self.title = 'System Input Sequencer'
        Builder.load_file('SIS_maker.kv')



Window.size = Window.size
Window.maximize()
Window.clearcolor = [0.2,0.2,0.22,1]
SIS_maker().run()

