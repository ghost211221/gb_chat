import inspect
from re import search, escape
import logging
logger = logging.getLogger('server')

class ServerMeta(type):
    """мета класс для проверки клиента"""
    def __init__(self, clsname, bases, clsdict):
        for method in clsdict:
            checkList = ["connect("]
            line = ""
            try:
                line = inspect.getsource(clsdict[method])
            except:
                pass
            for word in checkList: 
                self.__checkKeyword(line, word)

    def __checkKeyword(self, dataIn, etalonStr):
        if search(escape(etalonStr), dataIn):
            logger.critical(f'Обнаружен недопустимый вызов {etalonStr}.')
            exit(1)            