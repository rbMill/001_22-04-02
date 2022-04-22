from kivy.event import EventDispatcher


class example(EventDispatcher):
    def __init__(self):
        print(dir(self))
        help(self.fbind)
example()