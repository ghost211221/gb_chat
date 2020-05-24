import inspect
from re import search, escape
import logging
logger = logging.getLogger('client')

class ClientMeta(type):
    """мета класс для проверки клиента"""
    def __init__(self, clsname, bases, clsdict):
        for method in clsdict:
            checkList = ["accept(", "listen(", "socket("]
            line = ""
            try:
                line = inspect.getsource(clsdict[method])
            except:
                pass
            for word in checkList: 
                self.__checkKeyword(line, word)
            # print(method)
            # try:
            #     self.__checkKeyword(inspect.getsource(clsdict[method]), "accept(")
            #     self.__checkKeyword(inspect.getsource(clsdict[method]), "listen(")
            #     self.__checkKeyword(inspect.getsource(clsdict[method]), "socket(")
            # except TypeError:
            #     print(method, clsdict[method])

    def __checkKeyword(self, dataIn, etalonStr):
        if search(escape(etalonStr), dataIn):
            logger.critical(f'Обнаружен недопустимый вызов {etalonStr}.')
            exit(1)            
