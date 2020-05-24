# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 480)
        Dialog.setMinimumSize(QtCore.QSize(320, 480))
        Dialog.setMaximumSize(QtCore.QSize(320, 480))

        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(5, 5, 315, 475))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")

        self.photoLab = QtWidgets.QLabel(self.gridLayoutWidget)
        self.photoLab.setAlignment(QtCore.Qt.AlignCenter)
        self.photoLab.setObjectName("label")
        self.gridLayout.addWidget(self.photoLab, 1, 1, 1, 2)


        self.openFileButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.openFileButton.setObjectName("openFileButton")
        self.gridLayout.addWidget(self.openFileButton, 2, 1, 1, 1)

        self.gridLayout.setColumnStretch(2, 5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Профиль"))
        self.openFileButton.setText(_translate("Dialog", "Выбрать фото"))

    def closeWin(self, Dialog):
        Dialog.close()

