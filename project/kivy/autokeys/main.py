import regex
import math

from pynput.keyboard import Controller as Kcontrol,Key
from pynput.mouse import Controller as Mcontrol,Button as MButton

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle,Color
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
TextInput.halign = 'center'
TextInput.font_size = NumericProperty(17)
from kivy.config import Config
from kivy.core.window import Window
from kivy.base import Clock


class NumTextInput(TextInput):
    is_int = False
    funcs = lambda *args : None
    def __init__(self,**kwargs):
        try: self.is_int = kwargs.pop('is_int')
        except KeyError: pass
        try: self.funcs = kwargs.pop('funcs')
        except KeyError: pass
        super(NumTextInput, self).__init__(**kwargs)

    def insert_text(self, substring, from_undo=False):
        s = substring
        ch1 = regex.search('[0-9.]{1}',s)
        if self.is_int:
            ch1 = regex.search('[0-9]{1}', s)
        if ch1:
            return super(NumTextInput, self).insert_text(s,from_undo)

    def _on_focus(self, instance, value, *largs):
        super(NumTextInput, self)._on_focus(instance, value, *largs)
        if value:
            self.funcs()

class uilayout(GridLayout):
    def __init__(self,**kwargs):
        super(uilayout, self).__init__(**kwargs)
        self.force_stop = False
        self.cols = 2
        self.rows = 3
        self.DISPLAY = GridLayout(size_hint=[0.5, 0.33],rows=1,cols=3)
        self.add_widget(self.DISPLAY)

        self.START = Button(size_hint=[0.5, 0.33],text='START',on_press=self.start_event)
        self.add_widget(self.START)

        self.SETTINGS1 = GridLayout(size_hint=[0.5, 0.33],cols=2,rows=4)


        self.add_widget(self.SETTINGS1)

        self.RESET = Button(size_hint=[0.5, 0.33],text='RESET',on_press=self.restart)
        self.add_widget(self.RESET)

        self.SETTINGS2 = GridLayout(size_hint=[0.5, 0.33],cols=2,rows=4)
        self.add_widget(self.SETTINGS2)

        self.PAUSE = Button(size_hint=[0.5, 0.33],text='PAUSE',on_press=self.stop)
        self.add_widget(self.PAUSE)

        self.event_counter = 1
        self._cN = 1
        self.avoid_event = set(Clock.get_events())
        self.mouse = Mcontrol()
        self.keyboard = Kcontrol()
        self.prev_time_k = [Clock.get_time(),None]

        #Keyboard_lister
        self.kboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self.kboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self.kboard.bind(on_key_down=self._on_keyboard_down)

        Clock.schedule_once(self.settings1)

    def settings1(self,*args):
        self.avoid_event.update(Clock.get_events())
        self.dis1 = Label(text='0',size_hint=[1 / 3,1])
        self.DISPLAY.add_widget(self.dis1)

        self.dis2 = Widget( size_hint=[1 / 3, 1])
        self.DISPLAY.add_widget(self.dis2)



        self.dis3 = Label(text='0%', size_hint=[1 / 3, 1])
        self.DISPLAY.add_widget(self.dis3)

        self.SETTINGS1.add_widget(Label(text='Max Limit', size_hint=[0.75, 0.25]))
        self._limit = NumTextInput(size_hint=[0.25, 0.25],text='1000',is_int=True,funcs=self.restart)
        self.SETTINGS1.add_widget(self._limit)

        self.SETTINGS1.add_widget(Label(text='Time Interval(sec)', size_hint=[0.75, 0.25]))
        self._delay = NumTextInput(size_hint=[0.25, 0.25],text='0.5',funcs=self.restart)
        self.SETTINGS1.add_widget(self._delay)

        self.SETTINGS1.add_widget(Label(text='Delay on Start(sec)', size_hint=[0.75, 0.25]))
        self._delay_on_start = NumTextInput(size_hint=[0.25, 0.25],text='1',funcs=self.restart)
        self.SETTINGS1.add_widget(self._delay_on_start)

        self.SETTINGS1.add_widget(Label(text='Allow Left Click', size_hint=[0.75, 0.25]))
        self._allow_left_click = CheckBox(size_hint=[0.25, 0.25])
        self.SETTINGS1.add_widget(self._allow_left_click)

        self.SETTINGS2.add_widget(Label(text='Allow Space Bar', size_hint=[0.75, 0.25]))
        self._allow_space_bar = CheckBox(size_hint=[0.25, 0.25])
        self.SETTINGS2.add_widget(self._allow_space_bar)

        self.SETTINGS2.add_widget(Label(text='Allow Right Click', size_hint=[0.75, 0.25]))
        self._allow_right_click = CheckBox(size_hint=[0.25, 0.25])
        self.SETTINGS2.add_widget(self._allow_right_click)

        self.SETTINGS2.add_widget(Label(text='Allow "W" Key Press', size_hint=[0.75, 0.25]))
        self._allow_w_key = CheckBox(size_hint=[0.25, 0.25])
        self.SETTINGS2.add_widget(self._allow_w_key)

        self.SETTINGS2.add_widget(Label(text='Allow Enter Press', size_hint=[0.75, 0.25]))
        self._allow_enter_press = CheckBox(size_hint=[0.25, 0.25])
        self.SETTINGS2.add_widget(self._allow_enter_press)

    def start_event(self,*args):
        self.canC()
        self.force_stop = False
        try:
            interv = float(self._delay.text)
        except ValueError:
            self._delay.text = '0.5'
            return
        try:
            delay = float(self._delay_on_start.text)
        except ValueError:
            self._delay_on_start.text = '1'
            return
        lim = int(self._limit.text)
        if self.event_counter > lim:
            self.event_counter = 1
        def cycle(*args):
            sv = self.event_counter
            if sv >= lim+1:
                self.restart(neg=False)
                return False
            if self.force_stop:
                return False
            self.dis1.text = str(sv)
            self.dis3.text = str(round(sv/lim*100,2)) + '%'
            self.Graphics(neg=False)

            #Main Command Hear
            if self._allow_left_click.active:
                self.mouse.press(MButton.left)
                self.mouse.release(MButton.left)
            if self._allow_space_bar.active:
                self.keyboard.press(Key.space)
                self.keyboard.release(Key.space)
            if self._allow_right_click.active:
                self.mouse.press(MButton.right)
                self.mouse.release(MButton.right)
            if self._allow_w_key.active:
                self.keyboard.press('w')
                self.keyboard.release('w')
            if self._allow_enter_press.active:
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
            self.event_counter += 1
        self._clear()
        run_event = lambda *args:Clock.schedule_interval(cycle,interv)
        _ = Clock.schedule_once(run_event,delay)

    def stop(self,*args):
        self._clear()
        self.force_stop = True

    def restart(self,*args,**kwargs):
        neg = kwargs.get('neg',True)
        self.stop()
        if neg:
            self.dis1.text = '0'
            self.dis3.text = '0%'
        self.canC(neg=neg)
        self.event_counter = 1

    def canC(self,neg=True,*args):
        if self.event_counter != self._cN and neg:
            self.dis2.canvas.before.clear()

    def _clear(self,*args):
        for i in Clock.get_events():
            if i not in self.avoid_event:
                i.cancel()

    def Graphics(self,neg=True,*args):
        lim = int(self._limit.text)
        sec = self.event_counter
        self._cN = sec
        sec-=1
        [X,Y,],[W,H] = self.dis2.pos,self.dis2.size
        w = W*0.85
        h = H/lim*0.85
        x = X+0.15/2*W
        rt = sec/lim
        mp = math.pi/2.4
        dx = math.pi/2*rt
        r = math.cos(dx)
        g = math.cos(dx-mp)
        b = math.cos(dx-2*mp)
        try:
            y = Y+H*rt
        except ZeroDivisionError:
            y = Y
        with self.dis2.canvas.before:
            # Add a red color
            Color(r,g,b,1)
            # Add a rectangle
            Rectangle(pos=[x,y],size=[w,h])

    # kerboard listerner commands

    def _keyboard_closed(self):
        self.kboard.unbind(on_key_down=self._on_keyboard_down)
        self.kboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

        k = keycode[1]
        now = Clock.get_time()
        prevk = self.prev_time_k[1]
        dt = now - self.prev_time_k[0]

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if dt < 0.5:
            if prevk == 'alt':
                if k == 'f1':
                    self.stop()
                if k == 'f2':
                    self.restart()
                if k == 'f3':
                    self.start_event()
        if keycode[1] == 'escape':
            keyboard.release()
        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        self.prev_time_k = [now,k]
        return True

    # end

class AutoKeys(App):
    def build(self):
        con = Config
        con.set('graphics', 'width', '500')
        con.set('graphics', 'height', '500')
        con.set('graphics', 'resizable', '0')
        con.set('input', 'mouse', 'mouse,multitouch_on_demand')
        con.write()
        Window.clearcolor = [0.2,0.2,0.2,1]
        return uilayout()

AutoKeys().run()
