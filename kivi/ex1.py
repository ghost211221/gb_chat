from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
class Login_Screen(GridLayout):
   def __init__(self, **kwargs):
       super(Login_Screen, self).__init__(**kwargs)
       self.cols = 2
       self.add_widget(Label(text='User Name'))
       self.username = TextInput(multiline=False)
       self.add_widget(self.username)
       self.add_widget(Label(text='password'))
       self.password = TextInput(password=True, multiline=False)
       self.add_widget(self.password)
class AppKivy(App):
   def build(self):
       return Login_Screen()
if __name__ == '__main__':
   AppKivy().run()