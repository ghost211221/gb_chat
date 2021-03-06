import sys  # sys нужен для передачи argv в QApplication
import signal
from PyQt5 import QtWidgets

import socket
from serverGuiHandler import ServerGuiHandler

def main():

    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    # Создаём объект класса ExampleApp
    window = ServerGuiHandler()

    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
    