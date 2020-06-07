import re

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup


from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


from kivy.lang import Builder

from db_controller import DbController

Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<RV>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(24)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False
''')

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        rv.data[index]['selected'] = is_selected

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

        self.data = []

    def addItem(self, strIn, qIn):
        self.data.append({'text': f'{strIn}, {qIn}'})

    def delSelectedItem(self):
        for item in self.data:
            if item['selected']:
                return self.data.pop(self.data.index(item))

    def replaceItemByName(self, name, value):
        for item in self.data:
            if item['text'].startswith(f'{name}, '):
                self.data[self.data.index(item)]['text'] = f'{name}, {value}'


class FloatInput(TextInput):

    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)



class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.controller = DbController()

        #подписи над полями
        self.add_widget(Label(text='Список товаров', size_hint=(.4, .05), pos_hint={'x':.0, 'y':.95}))
        self.add_widget(Label(text='Введите новый товар', size_hint=(.4, .05), pos_hint={'x':.4, 'y':.95}))
        self.add_widget(Label(text='Введите количество', size_hint=(.2, .05), pos_hint={'x':.8, 'y':.95}))

        # поле ввода товара
        self.goodTi = TextInput(multiline=False, size_hint=(.4, .05), pos_hint={'x':.4, 'y':.9})
        self.add_widget(self.goodTi)

        # кнокпка добавления
        self.addGoodBtn =  Button(text='Добавить товар', size_hint=(.4, .05), pos_hint={'x':.4, 'y':.85})
        self.add_widget(self.addGoodBtn)
        self.addGoodBtn.bind(on_press=self.addGoodBtnCallback)

        # инпут для ввода количества
        self.quantitySpin = FloatInput(size_hint=(.2, .05), pos_hint={'x':.8, 'y':.9})

        self.add_widget(self.quantitySpin)

        self.list_view = RV(size_hint=(.4, .9), pos_hint={'x':.0, 'y':.05})
        self.add_widget(self.list_view)

        # кнокпка добавления
        self.delGoodBtn =  Button(text='Удалить товар', size_hint=(.4, .05), pos_hint={'x':.0, 'y':.0})
        self.add_widget(self.delGoodBtn)
        self.delGoodBtn.bind(on_press=self.delGoodBtnCallback)

        self.popup = Popup(title='Не хватает данных',
            content=Label(text='Для добавления в список введите название товара и его количество'),
            size_hint=(None, None), size=(600, 200)
        )

        self.setUp__listWidget()
        

    def addGoodBtnCallback(self, instance):
        if self.goodTi.text and  self.quantitySpin.text:
            good = self.goodTi.text
            quantity = self.quantitySpin.text
            self.goodTi.text = ''
            self.quantitySpin.text = ''

            item = self.controller.addItem(good, quantity)

            self.list_view.replaceItemByName(item['item'], item['quantity'])
            self.list_view.refresh_from_data()
        else:
            self.popup.open()        

    def delGoodBtnCallback(self, instance):
        itemLine = self.list_view.delSelectedItem()
        itemName = re.sub(r'[,\.0-9+-]+', '', itemLine)
        self.controller.deleteItem(itemName)
        

    def setUp__listWidget(self):
        goods = self.controller.getList()
        print(goods)
        if goods:
            for good in goods:
                self.list_view.addItem(good['item'], good['quantity'])