import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets

import socket
from clientGuiHandler import ClientGuiHandler

def main():

    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    # Создаём объект класса ExampleApp
    window = ClientGuiHandler()

    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == "__main__":
    main()