from socket import *
import sys
import time
import json

import threading

import hashlib
import hmac
import binascii

import base64
import re

from utils.variables import CONSTS, RESPONCES
from logs.client_logger import ClientLogger
from logs.logDecorator import LogDecorator
from descriptors.clientPort import ClientPort as Port
from meta.clientMeta import ClientMeta

from db.client.controller import Controller

@LogDecorator()
def getIP(args):
    if "-a" in args:
        idx = args.index("-a")
        return args[idx+1]
    else:
        return CONSTS["default-ip"]

@LogDecorator()
def getPort(args):
    if "-p" in args:
        idx = args.index("-p")
        return int(args[idx+1])
    else:
        return int(CONSTS["default-port"])

@LogDecorator()
def getName(args):
    if "-n" in args:
        idx = args.index("-n")
        return args[idx+1]
    else:
        return input('Введите свое имя: ')


class Client(metaclass=ClientMeta):
    """ класс клиента
    
    [description]
    
    Extends:
        metaclass=ClientMeta
    
    Variables:
        port {[type]} -- номер порта от 1204 до 65535
    """
    port = Port()

    def __init__(self, ip, port, name, socket, passwd, keys):
        self.logger = ClientLogger()
        self.ip = ip
        self.port = port
        self.name = name
        self.passwd = passwd
        self.keys = keys

        self.db_inst = Controller()

        self.__genPassHash()

        self.logger.LOGGER.info(f'попытка подключения к {self.ip}:{self.port} как {self.name}')
        print(f'попытка подключения к {self.ip}:{self.port} как {self.name}')

        self.socket = socket
        print(self.socket)
        self.socket.connect((self.ip, self.port))
        print(self.socket)

        self.contacts = []

    def __printHelp(self):
        """Функция выводящяя справку по использованию"""
        print('Поддерживаемые команды:')
        print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
        print('contacts - выести список контактов.')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')

    #########################################################################  

    def __printContacts(self):
        """Функция выводящяя список контактов пользователя"""
        print('Контакты:')
        for cont in self.contacts:
            print("cont: ", cont)
            print(f"\t{self.contacts.index(cont)}\t{cont['userName']}")

    def __addContact(self, contactName):
        """Функция добавляющая контакт в список контактов"""
        if contactName not in self.contacts:
            self.genAddContact(contactName)

    def __delContact(self, contactName):
        """Функция удаляющаяя контакт"""
        if contactName in self.contacts:
            self.genDelContact(contactName)

    def __genPassHash(self):        
        passwd_bytes = self.passwd.encode('utf-8')
        salt = self.name.lower().encode('utf-8')
        self.passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)

    #########################################################################

    @LogDecorator()
    def genPresence(self):
        """создание пресенс сообщения"""        
        pubkey = self.keys.publickey().export_key().decode('ascii')
        self.msg = {
            CONSTS["jim"]["action"]: CONSTS["jim"]["keys"]["presence"],
            CONSTS["jim"]["time"]: time.time(),
            CONSTS["jim"]["user"]: {
                CONSTS["jim"]["account"]: self.name,
                CONSTS["jim"]["pubkey"]: pubkey,                
            }
        }

    @LogDecorator()
    def genRegistration(self):
        """создание запроса на регистрацию"""
        self.msg = {
            CONSTS["jim"]["action"]: CONSTS["jim"]["keys"]["reg"],
            CONSTS["jim"]["time"]: time.time(),
            CONSTS["jim"]["user"]: {
                CONSTS["jim"]["account"]: self.name,                
                CONSTS["jim"]["passhash"]: binascii.hexlify(self.passwd_hash).decode('ascii'),
            }
        }

    @LogDecorator()
    def genReqContacts(self):
        """создание запроса списка контактов"""
        self.msg = {
            CONSTS["jim"]["action"]: CONSTS["jim"]["keys"]["get_contacts"],
            CONSTS["jim"]["time"]: time.time(),
            CONSTS["jim"]["user"]: {
                CONSTS["jim"]["account"]: self.name
            }
        }

    @LogDecorator()
    def genReqAvatar(self):
        """создание запроса аватара"""
        self.msg = {
            CONSTS["jim"]["action"]: CONSTS["jim"]["keys"]["get_avatar"],
            CONSTS["jim"]["time"]: time.time(),
            CONSTS["jim"]["user"]: {
                CONSTS["jim"]["account"]: self.name
            }
        }

    @LogDecorator()
    def genAddContact(self, contName):
        """создание запроса на добавление контакта"""
        self.msg = {
            CONSTS["jim"]["action"]: CONSTS["jim"]["keys"]["add_contact"],
            CONSTS["jim"]["time"]: time.time(),
            CONSTS["jim"]["account"]: contName,
            CONSTS["jim"]["user"]: {
                CONSTS["jim"]["account"]: self.name,        # contact owner
            }
        }

    @LogDecorator()
    def genDelContact(self, contName):
        """создание запроса на удаление контакта"""
        self.msg = {
            CONSTS["jim"]["action"]: CONSTS["jim"]["keys"]["del_contact"],
            CONSTS["jim"]["time"]: time.time(),
            CONSTS["jim"]["account"]: contName,
            CONSTS["jim"]["user"]: {
                CONSTS["jim"]["account"]: self.name
            }
        }

    @LogDecorator()
    def genExit(self):
        """создание сообщения о выходе"""
        self.msg = {
            CONSTS["jim"]["action"]: CONSTS["jim"]["keys"]["exit"],
            CONSTS["jim"]["time"]: time.time(),
            CONSTS["jim"]["account"]: self.name
        }

    @LogDecorator()
    def genNewAvatar(self, filename):
        """создание сообщения для отправки нового аватара"""
        img = None
        with open(filename, "rb") as file:
            img = file.read()

        self.msg = {
            CONSTS["jim"]["action"]: CONSTS["jim"]["keys"]["add_avatar"],
            CONSTS["jim"]["time"]: time.time(),
            CONSTS["jim"]["user"]: self.name,
            CONSTS["jim"]["keys"]["data"]: base64.b64encode(img).decode(CONSTS["encoding"])
        }

    #######################################################################
    
    @LogDecorator()
    def createMsg(self):
        to_user = input("Кому отправить: ")
        message = input("Введите сообщение: ")
        self.msg = {
            CONSTS["jim"]["action"]: CONSTS["jim"]["keys"]["message"],
            CONSTS["jim"]["time"]: time.time(),
            CONSTS["jim"]["sender"]: self.name,
            CONSTS["jim"]["destination"]: to_user,
            CONSTS["jim"]["keys"]["message_text"]: message
        }
        self.db_inst.add_history(self.name, to_user, message)
        self.logger.LOGGER.info(f'Сформирован словарь сообщения: {self.msg}')
        try:
            self.sendMsg()
            self.logger.LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
        except:
            self.logger.LOGGER.critical('Потеряно соединение с сервером.')
            sys.exit(1)
    
    @LogDecorator()
    def createMsg_(self, to_user, message):
        self.msg = {
            CONSTS["jim"]["action"]: CONSTS["jim"]["keys"]["message"],
            CONSTS["jim"]["time"]: time.time(),
            CONSTS["jim"]["sender"]: self.name,
            CONSTS["jim"]["destination"]: to_user,
            CONSTS["jim"]["keys"]["message_text"]: message
        }
        self.db_inst.add_history(self.name, to_user, message)
        self.logger.LOGGER.info(f'Сформирован словарь сообщения: {self.msg}')
        try:
            self.sendMsg()
            self.logger.LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
        except:
            self.logger.LOGGER.critical('Потеряно соединение с сервером.')
            sys.exit(1)
 
    @LogDecorator()   
    def processResp(self):
        """разбор ответа сервера на сообщение о присутствии"""
        self.logger.LOGGER.info(f'Разбираем ответ от сервера: {self.responce}')
        print(self.responce)
        if CONSTS["jim"]["keys"]["responce"] in self.responce:
            print("responce")
            if self.responce[CONSTS["jim"]["keys"]["responce"]] == 200:
                print("resp 200")
                return "200 : OK"
            elif self.responce[CONSTS["jim"]["keys"]["responce"]] == 202 and \
                "alert" in self.responce:
                print("contacts")
                self.contacts = self.responce['alert']
                return self.responce["alert"]
            elif self.responce[CONSTS["jim"]["keys"]["responce"]] == 203 and \
                "alert" in self.responce:
                return self.responce["alert"]
            elif self.responce[CONSTS["jim"]["keys"]["responce"]] == 400:
                print(f'400 : {self.responce[CONSTS["jim"]["keys"]["error"]]}')
                return f'400 : {self.responce[CONSTS["jim"]["keys"]["error"]]}'
            elif self.responce[CONSTS["jim"]["keys"]["responce"]] == 511:
                return 511
        raise ValueError

    @LogDecorator()   
    def processMsg(self):
        """обработка сообщений от пользователей"""
        # while True:
        try:
            self.getMsg()
            if CONSTS["jim"]["action"] in self.responce and \
                self.responce[CONSTS["jim"]["action"]] ==  CONSTS["jim"]["keys"]["message"] and \
                CONSTS["jim"]["sender"] in self.responce and \
                CONSTS["jim"]["destination"] in self.responce and \
                CONSTS["jim"]["keys"]["message_text"] in self.responce and \
                self.responce[CONSTS["jim"]["destination"]] ==  self.name:
                print(f'Получено сообщение от пользователя '
                    f'{self.responce[CONSTS["jim"]["sender"]]}'\
                    f':\n{self.responce[CONSTS["jim"]["keys"]["message_text"]]}'
                )
                self.logger.LOGGER.info(f'Получено сообщение от пользователя '
                    f'{self.responce[CONSTS["jim"]["sender"]]}'\
                    f':\n{self.responce[CONSTS["jim"]["keys"]["message_text"]]}'
                )
                return (self.responce[CONSTS["jim"]["sender"]], self.responce[CONSTS["jim"]["time"]], \
                    self.responce[CONSTS["jim"]["keys"]["message_text"]])
            else:
                self.logger.LOGGER.error(f'Получено некорректное сообщение с сервера: {self.responce}')
        except json.JSONDecodeError:
            self.logger.LOGGER.error(f'Не удалось декодировать полученное сообщение.')
        except(OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError):
            self.logger.LOGGER.critical(f'Потеряно соединение с сервером.')
            # break

########################################################################################

    @LogDecorator()
    def getMsg(self):
        """ получение сообщения
        
        Decorators:
            LogDecorator
        
        Raises:
            ValueError -- если сообщение не словарь - ошибка
        """
        respEnc = self.socket.recv(CONSTS["max-pack_len"])
        print(respEnc)
        if not  isinstance(respEnc, bytes):            
            self.logger.LOGGER.critical(f'сообщение не является байтами')
            raise ValueError
        self.responce = json.loads(respEnc.decode(CONSTS["encoding"]))
        print(self.responce)
        if not isinstance(self.responce, dict):            
            self.logger.LOGGER.critical(f'сообщение не является словарем')
            raise ValueError        

    # @LogDecorator()
    def sendMsg(self):
        """отправка сообщения self.msg"""
        self.socket.send(json.dumps(self.msg).encode(CONSTS["encoding"]))

#######################################################################################

    # @LogDecorator()
    # def userIneraction(self):
    #     self.__printHelp()
    #     while True:
    #         command = input('Введите команду: ')
    #         if command == 'message':
    #             self.createMsg()
    #         elif command == 'contacts':
    #             self.__printContacts()
    #         elif command == 'add_contact':
    #             self.__addContact()
    #         elif command == 'del_contact':
    #             self.__delContact()
    #         elif command == 'help':
    #             self.__printHelp()
    #         elif command == 'exit':
    #             self.genExit()
    #             self.sendMsg()
    #             print('Завершение соединения.')
    #             self.logger.LOGGER.info('Завершение работы по команде пользователя.')
    #             # Задержка неоходима, чтобы успело уйти сообщение о выходе
    #             time.sleep(0.5)
    #             break
    #         else:
    #             print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')

    def makePresence(self):
        """ действие присутствия """
        print("presense")
        self.genPresence()
        print("message: ", self.msg)
        self.sendMsg()
        self.getMsg()
        print("response: ", self.responce)

        res = self.processResp()
        print(f"res: {res}")
        if res == 511:
            return self.makeAuthorization()
        return f'400 : {self.responce[CONSTS["jim"]["keys"]["error"]]}'

    def makeAuthorization(self):
        """ действие авторизации """
        print("making authorization")
        data = self.responce[CONSTS["jim"]["keys"]["data"]]
        print(data)
        hash_ = hmac.new(binascii.hexlify(self.passwd_hash), data.encode('utf-8'))
        print(f"hash: {hash_}")
        digest = hash_.digest()
        self.msg = RESPONCES[ "resp_511"]
        self.msg[CONSTS["jim"]["keys"]["data"]] = binascii.b2a_base64(digest).decode('ascii')
        print(f"msg: {self.msg}")
        self.sendMsg()
        self.getMsg()
        print("response: ", self.responce)
        return self.processResp()

    def makeRegister(self):
        """ действие регистрации """
        self.genRegistration()
        print("message: ", self.msg)
        self.sendMsg()
        self.getMsg()
        print("response: ", self.responce)
        return self.processResp()

    def makeAddContact(self, contact):
        """ действие добавление контакта contact """
        self.genAddContact(contact)
        print("message: ", self.msg)
        self.sendMsg()
        self.getMsg()
        print("response: ", self.responce)
        return self.processResp()


    def getContacts(self):
        self.genReqContacts()
        print("message: ", self.msg)
        self.sendMsg()
        self.getMsg()
        self.contacts = self.processResp()
        return self.contacts


    def getAvatar(self):
        self.genReqAvatar()
        print("message: ", self.msg)
        self.sendMsg()
        self.getMsg()

        resp = self.processResp()
        if resp:
            ans = resp[0]
            missing_padding = 4-len (resp[0])% 4 
            print(f"missing padding {missing_padding}")
            if missing_padding: 
                ans += '=' * missing_padding 

            return base64.b64decode(ans.encode(CONSTS['encoding']))

    def makeExit(self):        
        self.genExit()
        print(self.msg)
        self.sendMsg()
        print('Завершение соединения.')
        self.logger.LOGGER.info('Завершение работы по команде пользователя.')
        # Задержка неоходима, чтобы успело уйти сообщение о выходе
        time.sleep(0.5)


    def mainLoop(self):
        # пресенс сообщение
        self.genPresence()
        print("message: ", self.msg)
        self.sendMsg()
        self.getMsg()
        print("response: ", self.responce)
        print(self.processResp())
        # запрос списка контактов
        self.genReqContacts()
        print("message: ", self.msg)
        self.sendMsg()
        self.getMsg()
        self.contacts = self.processResp()
        self.__printContacts()
        # прием сообщений
        self.receiver = threading.Thread(target=self.processMsg, args=())
        self.receiver.daemon = True
        self.receiver.start()

        # взаимодействие с пользователем и отправка сообщений
        self.userItf = threading.Thread(target=self.userIneraction, args=())
        self.userItf.daemon = True
        self.userItf.start()

        self.logger.LOGGER.debug('Запущены процессы')

        # Watchdog основной цикл, если один из потоков завершён,
        # то значит или потеряно соединение или пользователь
        # ввёл exit. Поскольку все события обработываются в потоках,
        # достаточно просто завершить цикл.
        while True:
            time.sleep(1)
            if self.receiver.is_alive() and self.userItf.is_alive():
                continue
            break
        

if __name__ == "__main__":
    ip = getIP(sys.argv)
    port = getPort(sys.argv)
    name = getName(sys.argv)
    clientIsnt = Client(ip, port, name, socket(AF_INET, SOCK_STREAM))