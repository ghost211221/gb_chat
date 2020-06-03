from PyQt5 import QtCore, QtGui, QtWidgets

from db_controller import DbController
from goodsGui import Ui_MainWindow


class GoodsGuiHandler(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.controller = DbController()

        # запускаем настройки
        self.setUp__addItemBtn()

        self.setUp__delItemBtn()

        self.setUp__listWidget()

    def setUp__addItemBtn(self):
        self.addItemBtn.clicked.connect(self.addItemToListEval)

    def setUp__delItemBtn(self):
        self.delItemBtn.clicked.connect(self.delItemsFromListEval)

    def setUp__listWidget(self):
        goods = self.controller.getList()
        if goods:
            self.listWidget.addItems(goods)

###########################################################################
    
    def addItemToListEval(self):
        text = self.itemLE.text()
        if text:
            self.listWidget.addItem(text)
            self.controller.addItem(text)

        self.itemLE.clear()

    def delItemsFromListEval(self):
        self.controller.deleteItem(self.listWidget.currentItem().text())

        self.listWidget.takeItem(self.listWidget.currentRow())
