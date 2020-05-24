#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PIL import Image, ImageDraw #Подключим необходимые библиотеки.
from PIL.ImageQt import ImageQt

from PyQt5.QtWidgets import (QMainWindow, QHBoxLayout, QTextEdit, QLabel,
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QPixmap, QIcon


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.lbl = QLabel(self)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Открыть файл')
        openFile.triggered.connect(self.showDialog)

        sepia_btn = QAction('Sepia', self)
        sepia_btn.setStatusTip('Эффект сепия')
        sepia_btn.triggered.connect(self.actionSepia) 

        negative_btn = QAction('Negative', self)
        negative_btn.setStatusTip('Эффект негатива')
        negative_btn.triggered.connect(self.actionNegative)        

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Файл')
        fileMenu.addAction(openFile)

        menubar.addAction(sepia_btn)
        menubar.addAction(negative_btn)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

    def actionSepia(self):
        self.init_pix()
        
        for i in range(self.width):
            for j in range(self.height):
                a = self.pix[i, j][0]
                b = self.pix[i, j][1]
                c = self.pix[i, j][2]
                S = (a + b + c)
                a = S + self.depth * 2
                b = S + self.depth
                c = S
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                self.draw.point((i, j), (a, b, c))

        self.img_tmp = ImageQt(self.img_tmp.convert('RGBA'))
        self.pixmap = QPixmap.fromImage(self.img_tmp)
        self.show_image()

    def actionNegative(self):
        self.init_pix()
        
        for i in range(self.width):
            for j in range(self.height):
                a = self.pix[i, j][0]
                b = self.pix[i, j][1]
                c = self.pix[i, j][2]
                self.draw.point((i, j), (255 - a, 255 - b, 255 - c))

        self.img_tmp = ImageQt(self.img_tmp.convert('RGBA'))
        self.pixmap = QPixmap.fromImage(self.img_tmp)
        self.show_image()


    def showDialog(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]

        self.pixmap = QPixmap(self.fname)
        self.lbl.resize(300,300)
        self.show_image()

    def init_pix(self):
        image = Image.open(self.fname)
        self.img_tmp = image
        self.draw = ImageDraw.Draw(self.img_tmp)
        self.width = self.img_tmp.size[0]
        self.height = self.img_tmp.size[1]
        self.pix = self.img_tmp.load()
        self.depth = 30


    def show_image(self):
        self.lbl.setPixmap(self.pixmap)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
