from kivy.app import App

from kivyGoodsCui import MainScreen

class AppKivy(App):
    
   def build(self):
       return MainScreen()

if __name__ == '__main__':
   AppKivy().run()