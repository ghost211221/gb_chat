import sys
import os
import logging
# sys.path.append('../')
from utils.variables import CONSTS


class ClientLogger():
    def __init__(self):
        # создаём формировщик логов (formatter):
        self.CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

        # Подготовка имени файла для логирования
        # self.PATH = os.path.dirname(os.path.abspath(__file__))
        # self.PATH = os.path.join(self.PATH, 'client.log')

        # создаём потоки вывода логов
        # self.STREAM_HANDLER = logging.StreamHandler(sys.stderr)
        # self.STREAM_HANDLER.setFormatter(self.CLIENT_FORMATTER)
        # self.STREAM_HANDLER.setLevel(CONSTS["logging_level"])
        self.LOG_FILE = logging.FileHandler('client.log', encoding='utf8')
        self.LOG_FILE.setFormatter(self.CLIENT_FORMATTER)

        # создаём регистратор и настраиваем его
        self.LOGGER = logging.getLogger('client')
        # self.LOGGER.addHandler(self.STREAM_HANDLER)
        self.LOGGER.addHandler(self.LOG_FILE)
        self.LOGGER.setLevel(CONSTS["logging_level"])

