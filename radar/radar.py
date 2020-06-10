import random

from math import cos, sin, pi, sqrt, asin

import kivy  
from kivy.app import App  
from kivy.uix.widget import Widget 
from kivy.graphics import Rectangle, Color, Line
from kivy.clock import Clock
kivy.require("1.9.1")  

class CanvasWidget(Widget): 

    def __init__(self, **kwargs):

        self.x1, self.y1 = 500, 200
        self.fi = 0

        super(CanvasWidget, self).__init__(**kwargs) 
  
        with self.canvas: 
            Color(0, 1, 1, 1)
  
            self.rect = Rectangle(pos=(self.x1, self.y1), size=(6, 6))
  
            self.bind(pos = self.update_rect1, size = self.update_rect1) 

            self.radius = 300

            Color(0, 1, 0, 1)
            self.line = Line(points=[400, 300, 700, 300], width=2)
  
    def update_rect1(self, *args):
        if self.fi == 0:
            r = random.randint(100,250)
            self.x1 = 400 + r * cos(self.fi)
            self.y1 = 300 + r * sin(self.fi)

            self.rect.pos = (self.x1, self.y1)
            Color(0, 1, 1, 1)


    def update_line(self, *args):
        self.x = 400 + self.radius * cos(2 * pi * self.fi / 360)
        self.y = 300 + self.radius * sin(2 * pi * self.fi / 360)
        self.fi = (self.fi + 2) % 360
        self.line.points = [400, 300, self.x, self.y]
        self.line.width = 2
  
class CanvasApp(App): 
    def build(self): 
        self.game = CanvasWidget()
        Clock.schedule_interval(self.game.update_line, 1.0 / 10.0)
        Clock.schedule_interval(self.game.update_rect1, 1.0 / 10.0)

        return self.game
CanvasApp().run() 