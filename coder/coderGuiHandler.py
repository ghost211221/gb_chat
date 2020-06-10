from PyQt5 import QtCore, QtGui, QtWidgets

from coderGui import Ui_MainWindow

from utils import encrypt


class CoderGuiHandler(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        # запускаем настройки
        self.setUp__coderBtn()

    def setUp__coderBtn(self):
        self.codeBtn.clicked.connect(self.codeTextEval)

###########################################################################
    
    def codeTextEval(self):
        initText = self.initTE.toPlainText()

        codedText = encrypt(initText, '2020')

        self.codedTE.setPlainText(codedText)
