from sys import argv, path, _getframe
path.append('../')

from logs.client_logger import ClientLogger

class LogDecorator():
    def __init__(self):
        self.logger = ClientLogger()

    def __call__(self, func):
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)

            self.logger.LOGGER.info(f'Была вызвана функция {func.__name__} c параметрами \
                {args}, {kwargs}.\nВызов из модуля {func.__module__}')

            # print(_getframe(1).f_code.co_name)
            return res
        return decorated
