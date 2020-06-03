# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'goodsGui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.mainGrid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.mainGrid.setContentsMargins(5, 5, 5, 5)
        self.mainGrid.setHorizontalSpacing(5)
        self.mainGrid.setVerticalSpacing(3)
        self.mainGrid.setObjectName("mainGrid")
        self.itemLE = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.itemLE.setObjectName("itemLE")
        self.mainGrid.addWidget(self.itemLE, 1, 1, 1, 2)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.mainGrid.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.mainGrid.addWidget(self.label_2, 0, 1, 1, 2)
        self.listWidget = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget.setObjectName("listWidget")
        self.mainGrid.addWidget(self.listWidget, 1, 0, 4, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainGrid.addItem(spacerItem, 4, 1, 1, 1)
        self.delItemBtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.delItemBtn.setObjectName("delItemBtn")
        self.mainGrid.addWidget(self.delItemBtn, 2, 1, 1, 1)
        self.addItemBtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.addItemBtn.setObjectName("addItemBtn")
        self.mainGrid.addWidget(self.addItemBtn, 2, 2, 1, 1)
        self.mainGrid.setColumnStretch(0, 2)
        self.mainGrid.setColumnStretch(1, 1)
        self.mainGrid.setColumnStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "List of goods"))
        self.label.setText(_translate("MainWindow", "Список покупок"))
        self.label_2.setText(_translate("MainWindow", "Новый товар"))
        self.delItemBtn.setText(_translate("MainWindow", "Удалить"))
        self.addItemBtn.setText(_translate("MainWindow", "Добавить"))


