from PyQt5 import QtCore, QtGui, QtWidgets

import threading

from server import Server
from db.server.controller import Controller
from serverWin import Ui_ServerGui

class ServerGuiHandler(QtWidgets.QMainWindow, Ui_ServerGui):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.db_inst = Controller()

        self.setUp_serverStartBtn()
        self.setUp_refreshBtn()

        self.setUp_clientsList()

        self.selectedUser = ""

    def setUp_refreshBtn(self):        
        self.refreshBtn.clicked.connect(self.setUp_clientsList)
        self.refreshBtn.clicked.connect(self.showStatistic)

    def setUp_serverStartBtn(self):        
        self.serverStartBt.clicked.connect(self.startServer)   

    def startServer(self):
        self.serverInst = Server(self.portSpin.value())        
        self.server = threading.Thread(target=self.serverInst.runServer, args=())
        self.server.daemon = True
        self.server.start()
        self.serverStartBt.setEnabled(False)
        self.serverStatudLab.setText("сервер запущен")

    def setUp_clientsList(self):
        self.clientsList.clear()
        users = self.db_inst.read_users()
        [self.clientsList.addItem(user.userName) for user in users]

        self.clientsList.itemClicked.connect(self.showStatistic)        

    def showStatistic(self):        
        if self.sender().objectName() == "clientsList":
            self.selectedUser = self.sender().currentItem().text()
            print(self.selectedUser)
            if self.selectedUser:
                self.staticticTable.clearContents()
                statistic = self.db_inst.read_history(self.selectedUser)
                print(statistic)
                for i in range(len(statistic)):
                    self.staticticTable.insertRow(i)
                    print(statistic[i])
                    print(self.selectedUser, statistic[i].userStoriesIP, statistic[i].userStoriesPort, statistic[i].userStoriesTime)
                    self.staticticTable.setItem(i, 0, QtWidgets.QTableWidgetItem(self.selectedUser))
                    self.staticticTable.setItem(i, 1, QtWidgets.QTableWidgetItem(statistic[i].userStoriesIP))
                    self.staticticTable.setItem(i, 2, QtWidgets.QTableWidgetItem(statistic[i].userStoriesPort))
                    self.staticticTable.setItem(i, 3, QtWidgets.QTableWidgetItem(str(statistic[i].userStoriesTime)))
                    