import logging
logger = logging.getLogger('server')

class ServerPort:
    """дескриптор порта    
    [description]
    если порт не в диапазоне 1023 - 65536 -> ошибка
    """
    def __set__(self, inst : object, value : int) -> None:
        print("port descriptor")
        print(value)
        if not 1023 < value < 65536:
            logger.critical(
                f'Запуска сервера с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535.')
            exit(1)
        # Если порт прошел проверку, добавляем его в список атрибутов экземпляра
        inst.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        # owner - <class '__main__.Server'>
        # name - port
        self.name = name