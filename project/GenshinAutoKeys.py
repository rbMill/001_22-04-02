import threading
import time
import tkinter
from ctypes import windll
from tkinter import *

from pynput.keyboard import Controller,Key
from pynput.mouse import Controller,Button
import myLibrary
import keyboard
import pynput.keyboard
from myLibrary import *

global ENDFLAG
ENDFLAG = False

class GenshinAuto():
    def __init__(self):
        windll.shcore.SetProcessDpiAwareness(1)
        self.root = Tk()

        self.keyboard = pynput.keyboard.Controller()
        self.mouse = pynput.mouse.Controller()

        self.root.title('GenshinAutoKeys')
        self.root.iconbitmap('Paimon.ico')
        self.root.geometry('676x432')

        self.root.resizable(False,False)

        self.DisplayFrame = Frame(self.root,bg="#A0A0A0",width=500,height=130)

        self.MouseVar  = tkinter.BooleanVar()
        self.MouseAllow = Checkbutton(self.root,text='LMC',bg='#DAC190',fg='BLACK',font=('Adobe',8)
                                      ,variable=self.MouseVar)
        self.SpaceVar = tkinter.BooleanVar()
        self.SpaceAllow = Checkbutton(self.root, text='SPACE', bg='#DAC190', fg='BLACK', font=('Adobe', 8)
                                      ,variable=self.SpaceVar)

        self.disLx, self.disLy  = 510, 130
        self.Display = Canvas(self.root,bg="#A0A0A0",width=self.disLx,height=self.disLy)

        self.Lims1 = Entry(self.root,bg='#5E6A7B',justify=CENTER,fg='black',width=4,font=('Adobe',12))
        self.Lims2 = Entry(self.root,bg='#785E7B',justify=CENTER,fg='black',width=4,font=('Adobe',12))
        #Variables
        self.pastI = 0
        self.I = 0
        self.Duration = 120
        self.Delay = 0.5
        self.STARTKEY = 'F1'
        self.STOPKEY = 'F2'
        self.ENDKEY = 'F3'

        self.LOOP = threading.Thread(target=self._loop)
        self.LOOP.setName('LoopThread')
        self.LOOP.daemon = True
        self.PlayButton = tkinter.Button(self.root,text='  PLAY  ',bg='#65DE87',fg='#EFEFEF',font=('Impact',12)
                                ,command=lambda : self.eventHandle('play'))
        self.StopButton = tkinter.Button(self.root, text='  STOP  ', bg='#FF1818',fg='#EFEFEF', font=('Impact', 12)
                                ,command=lambda : self.eventHandle('pause'))
        self.EndButton = tkinter.Button(self.root, text='  END  ', bg='#494949',fg='#EFEFEF', font=('Impact', 12)
                                ,command=lambda : self.eventHandle('stop'))
        self.mainloop()

    def eventHandle(self,by):
        ofl = list(map(lambda e:e.name,threading.enumerate()))
        print(' '.join(ofl),by,self.pastI)
        if by == 'play':
            self.I = self.pastI
            if ofl.count('LoopThread') == 0:
                self.LOOP.start()
            elif self.I != self.Duration:
                self.I = self.pastI
            elif self.I == self.Duration:
                self.I = 0
        elif by == 'pause':
            if self.I != self.Duration:
                self.pastI = self.I
            self.I = self.Duration
        elif by == 'stop':
            self.I = self.Duration
            self.pastI = 0


    def _loop(self):
        try:
            while True:
                if globals()['ENDFLAG'] == True:
                    break
                    raise ValueError
                if self.I != self.Duration:
                    while self.I != self.Duration:
                        try:
                            self.Duration = int(self.Lims1.get())
                            if self.Duration < 1:
                                self.Duration = 1
                            elif self.Duration > 500:
                                self.Duration = 500
                        except ValueError:
                            pass
                        try:
                            self.Delay = float(self.Lims2.get())
                            if self.Delay < 0.05:
                                self.Delay = 0.1
                        except ValueError:
                            pass
                        if self.SpaceVar.get() == True:
                            self.keyboard.press(Key.space)
                            self.keyboard.release(Key.space)
                        if self.MouseVar.get() == True:
                            self.mouse.press(Button.left)
                            self.mouse.release(Button.left)
                        if self.I < self.Duration:
                            self.Display.delete(ALL)
                            self.Display.create_line(0,self.disLy*0.5,self.I,self.disLy*0.5,fill='#8DFF00')
                            self.Display.create_line(self.I, self.disLy * 0.5, self.I, self.disLy * 0.25,fill='#8DFF00')
                            self.Display.create_line(self.I,self.disLy*0.25,self.I+10,self.disLy*0.25,fill='#8DFF00')
                            self.Display.create_line(self.I + 10, self.disLy * 0.25, self.I + 10, self.disLy * 0.5,fill='#8DFF00')
                            self.Display.create_line(self.I + 10, self.disLy * 0.5,self.disLx,self.disLy*0.5,fill='#8DFF00')

                            self.Display.create_line(self.Duration+5,0,self.Duration+5,self.disLy,fill='red')

                            self.I+=1
                        try:
                            time.sleep(self.Delay)
                        except ValueError:
                            time.sleep(0.1)
                    print("ENDED",self.I,self.Duration)
        except RuntimeError or TclError:
            return


    def mainloop(self):
        myLibrary.TkinterMethods.DefaultText(self.Lims1, '120')
        TkinterMethods.DefaultText(self.Lims2, '0.5')
        self.Lims1.bind('<Any-KeyRelease>',lambda e:myLibrary.TkinterMethods.DefaultText(self.Lims1, '120',active=('black','#5E6A7B')))
        self.Lims2.bind('<Any-KeyRelease>',lambda e:myLibrary.TkinterMethods.DefaultText(self.Lims2, '0.5',active=('black','#785E7B')))
        self.MouseAllow.grid(column=0,row=0,columnspan=2,sticky=NSEW)
        self.SpaceAllow.grid(column=0, row=1,columnspan=2,sticky=NSEW)
        self.Display.grid(column=2,row=0,columnspan=3,rowspan=2)

        self.Lims1.grid(column=0,row=3,sticky=NSEW)
        self.Lims2.grid(column=1, row=3, sticky=NSEW)
        self.PlayButton.grid(column=2,row=3,sticky=NSEW)
        self.StopButton.grid(column=3,row=3,sticky=NSEW)
        self.EndButton.grid(column=4,row=3,sticky=NSEW)

        self.root.bind(f'<KeyRelease-{self.STARTKEY}>',lambda e:self.eventHandle('play'))
        self.root.bind(f'<KeyRelease-{self.STOPKEY}>', lambda e: self.eventHandle('pause'))
        self.root.bind(f'<KeyRelease-{self.ENDKEY}>', lambda e: self.eventHandle('stop'))

        self.root.mainloop()

if __name__ == '__main__':
    print(list(map(lambda e: e.name, threading.enumerate())))
    try:
        GenshinAuto()
    except RuntimeError:
        pass
    globals()['ENDFLAG'] = True
    print(list(map(lambda e: e.name, threading.enumerate())))
