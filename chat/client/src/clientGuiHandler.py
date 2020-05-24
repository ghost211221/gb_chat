from PyQt5 import QtCore, QtGui, QtWidgets

from socket import socket, AF_INET, SOCK_STREAM

import datetime

import threading

import re

from client import Client
from db.client.controller import Controller
from clientWin import Ui_MainWindow
from utils.keys_gen import gen_keys


from profile    import Ui_Dialog as profileWinCls

from photoHandler import make_shaped_photo

class ClientGuiHandler(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.db_inst = Controller()

        self.profileWinObj      = profileWinCls()

        self.profileForm = None

        # активный чат
        self.selectedUser = ""
        self.nickName = ""

        self.contacts = []

        # доп окна
        self.initProfileWin()


        # запускаем настройки
        self.setUp__connectBtn()

        self.setUp__profileBtn()

        self.setUp__contactsList()

        self.setup__sendMsgBtn()

        self.setup__addContactBtn()

        self.setup__formatBtns()

        self.setup__smilesBtns()

        self.setup__profileOpenFileButton()


    def closeEvent(self, event):
        """ обрабатываем событие нажатия на главную кнопку закрытия окна """
        print("User has clicked the red x on the main window")
        event.accept()        
        self.close_application()
        try:
            self.clientIsnt.makeExit()
        except:
            pass

        app = QtWidgets.QApplication.instance()
        app.closeAllWindows()

    def setUp__connectBtn(self):
        self.connectBtn.clicked.connect(self.connectToServer)   

    def setUp__profileBtn(self):
        self.profileBtn.clicked.connect(self.evalShowProfile)   

    def setUp__contactsList(self):
        self.conttactsList.doubleClicked.connect(self.evalContactSelect)

    def setup__sendMsgBtn(self):
        self.sendMsgBtn.clicked.connect(self.evalSendMsg)

    def setup__addContactBtn(self):
        self.addContactBtn.clicked.connect(self.evalAddContact)

    def setup__formatBtns(self):
        self.boldBtn.clicked.connect(self.evalBoldToggle)
        self.italicBtn.clicked.connect(self.evalItalicToggle)
        self.underlineBtn.clicked.connect(self.evalUnderlineToggle)

    def setup__smilesBtns(self):
        self.smileBtn.clicked.connect(self.evalSmile)
        self.sadBtn.clicked.connect(self.evalSad)
        self.surprizeBtn.clicked.connect(self.evalSurprize)

    def setup__profileOpenFileButton(self):
        self.profileWinCls_ui.openFileButton.clicked.connect(self.evalSelectPhoto)


######################################################################
    def close_application(self):
        self.profileForm.close()
        exit()

    def initProfileWin(self):
        self.profileForm  = QtWidgets.QDialog()
        self.profileWinCls_ui = profileWinCls()        
        self.profileWinCls_ui.setupUi(self.profileForm)

#######################################################################
    def evalShowProfile(self):
        if self.profileForm:
            self.profileForm.close()

        if self.profileWinCls_ui:
            self.profileForm.show()

    def evalBoldToggle(self):
        self.mainFont.setBold(not self.mainFont.bold())
        self.messageTE.setFont(self.mainFont)

    def evalItalicToggle(self):
        self.mainFont.setItalic(not self.mainFont.italic())
        self.messageTE.setFont(self.mainFont)

    def evalUnderlineToggle(self):
        self.mainFont.setUnderline(not self.mainFont.underline())
        self.messageTE.setFont(self.mainFont)

    def evalSmile(self):
        url = 'imgs/smiles/ab.gif'
        self.messageTE.insertHtml('<img src="%s" />' % url)

    def evalSad(self):
        url = 'imgs/smiles/ac.gif'
        self.messageTE.insertHtml('<img src="%s" />' % url)

    def evalSurprize(self):
        url = 'imgs/smiles/ai.gif'
        self.messageTE.insertHtml('<img src="%s" />' % url)

    def evalSelectPhoto(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        pixmap = QtGui.QPixmap.fromImage(make_shaped_photo(fname))
        self.profileWinCls_ui.photoLab.setPixmap(pixmap)
        self.clientIsnt.genNewAvatar(fname)
        self.clientIsnt.sendMsg()

    def connectToServer(self):
        self.nickName = self.nickLE.text()
        self.passwd = self.passLE.text()
        if self.nickName:
            port = self.portSpin.value()
            ip = self.ipLE.text()
            if self.passwd:            
                try:
                    self.clientIsnt = Client(ip, port, self.nickName,
                        socket(AF_INET, SOCK_STREAM), self.passwd, gen_keys(self.nickName))
                    self.evalConnection()
                    print("connected")
                    self.profileBtn.setEnabled(True)
                    print("btn enabled")

                    self.contacts = self.clientIsnt.getContacts()
                    print("contacts")
                    self.avatar = self.clientIsnt.getAvatar()
                    print("avatar")
                    if self.avatar:
                        print("avatar")
                        qimg = QtGui.QImage.fromData(self.avatar[0])
                        self.profileWinCls_ui.photoLab.setPixmap(QtGui.QPixmap.fromImage(qimg))
                        print("pixmap")

                    [self.conttactsList.addItem(contact["userName"]) for contact in self.contacts]

                    self.receiver = threading.Thread(target=self.recHandler, args=())
                    self.receiver.daemon = True
                    self.receiver.start()
                except ConnectionError:
                    QtWidgets.QMessageBox.information(self, 'Ошибка', 'Не могу подключиться к серверу')
            else:
                QtWidgets.QMessageBox.information(self, 'Пароль', 'Введите пароль')
        else:            
            QtWidgets.QMessageBox.information(self, 'Имя пользователя', 'Укажаите имя перед подключением.')


    def evalContactSelect(self):        
        self.selectedUser = self.sender().currentItem().text()
        self.contactLab.setText(f"Чат с {self.selectedUser}")
        # не получилось отсортировать по времени отправки сообщения
        story = self.db_inst.read_history(self.nickName, self.selectedUser) + self.db_inst.read_history(self.selectedUser, self.nickName)
        # story = sorted(self.db_inst.read_history(self.nickName, self.selectedUser) + self.db_inst.read_history(self.selectedUser, self.nickName),
        #     key=lambda k: k.StoryTime)
        for msg in story:
            self.chatTE.insertHtml(f" <br>{msg.StorySend} {msg.StoryTime} <br>")
            self.chatTE.insertHtml(msg.StoryMessage)
            self.chatTE.insertHtml("<br>")

    def evalSendMsg(self):
        msg = self.messageTE.toHtml()
        self.messageTE.clear()
        self.clientIsnt.createMsg_(self.selectedUser, msg)        
        self.chatTE.insertHtml(f"{self.nickName} {datetime.datetime.now()} <br>")
        self.chatTE.insertHtml(msg)
        self.chatTE.insertHtml("<br>")

    def recHandler(self):
        """ обертка для приема сообщений и добавления в окно чата """
        while True:
            msg = self.clientIsnt.processMsg()
            if msg:
                if msg[0] == self.selectedUser:
                    # если сообщение идет в активный чат, сразу отображаем
                    self.chatTE.append(f"{msg[0]} {msg[1]}\n{msg[2]}\n")
                # сохраняем полученное сообщение в базу
                self.db_inst.add_history(msg[0], self.nickName, msg[2])
                if msg[0] not in self.contacts:
                    # если сообщение от неизвестного контакта:
                    # добавляем в список
                    # сохраняем контакт в базе
                    self.contacts.append(msg[0])
                    self.conttactsList.clear()
                    print(self.contacts)
                    [self.conttactsList.addItem(contact) for contact in self.contacts]
                    self.clientIsnt.makeAddContact(msg[0])

    def evalConnection(self):
        """ запуск авторизации/регистрации """
        resp =  self.clientIsnt.makePresence()
        print(resp)
        if re.search(r'400 : Пользователь не зарегистрирован', resp):
            # регестрируемся
            print("register")
            self.clientIsnt.makeRegister()
            self.clientIsnt.makePresence()

    def evalAddContact(self):        
        contName = self.newContactLE.text()
        if contName:
            self.clientIsnt.makeAddContact(contName)
        else:
            QtWidgets.QMessageBox.information(self, 'Упс', 'Контакт не найден')
   