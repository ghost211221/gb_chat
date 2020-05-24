from socket import *
import sys
import os
import json

import select
import hmac
import hashlib
import binascii

import base64

from utils.variables import CONSTS, RESPONCES
# from logs.server_logger import ServerLogger
from logs.logDecorator import LogDecorator
from descriptors.serverPort import ServerPort as Port
from meta.serverMeta import ServerMeta

from db.server.controller import Controller

from decorators.login_required import LoginRequired


@LogDecorator()
def getPort(args):
    if "-p" in args:
        idx = args.index("-p")
        return int(args[idx+1])
    else:
        return int(CONSTS["default-port"])

class Server(metaclass=ServerMeta):
    """[summary]
    [description]
    """
    port = Port()
    def __init__(self, port):
        self.port = port
        print(f"port: {port}")
        # self.logger = ServerLogger()      
        
        self.db_inst = Controller()

        self.clients = []
        self.names = {}
        self.messages_list = []

        self.__genSock()
        print(self.socket)
        # self.runServer()

    @LogDecorator()
    def __genSock(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.socket.listen(CONSTS["max-connections"])
        self.socket.settimeout(0.1)

    @LogDecorator()
    def sendMsg(self, client, message):
        print("sending message")
        print(client)
        print(message)
        print("==========================================")
        client.send(json.dumps(message).encode(CONSTS["encoding"]))   

    @LogDecorator()
    def getMsg(self, client):
        msgEnc = client.recv(CONSTS["max-pack_len"])
        print("сообщение от клиента")
        print(msgEnc)
        if not  isinstance(msgEnc, bytes):            
            # self.logger.LOGGER.critical(f'сообщение не является байтами')
            raise ValueError
        msg = json.loads(msgEnc.decode(CONSTS["encoding"]))
        print(msg)
        if not isinstance(msg, dict):
            # self.logger.LOGGER.critical(f'сообщение не является словарем')
            raise ValueError               
        print("-------------------------------------")
        return msg

####################################################################################################

    def getContacts(self, clientName):
        """ получение списка контактов клиента по имени"""        
        self.db_inst.user_contacts(clientName)


####################################################################################################

    # @LogDecorator()
    @LoginRequired()
    def process_client_msg(self, message, client):        
        # Если это сообщение о присутствии, принимаем и отвечаем, если успех
        print("обработка сообщения от {client}")
        print(message)
        if CONSTS["jim"]["action"] in message and \
            message[CONSTS["jim"]["action"]] == CONSTS["jim"]["keys"]["presence"] and \
            CONSTS["jim"]["time"] in message and CONSTS["jim"]["user"] in message:

            self.authorize(message, client)
            
        elif CONSTS["jim"]["action"] in message and \
            message[CONSTS["jim"]["action"]] == CONSTS["jim"]["keys"]["reg"] and \
            CONSTS["jim"]["time"] in message and CONSTS["jim"]["user"] in message:

            self.registration(message, client)

        # получаем список контактов
        elif CONSTS["jim"]["action"] in message and \
            message[CONSTS["jim"]["action"]] == CONSTS["jim"]["keys"]["get_contacts"] and \
            CONSTS["jim"]["time"] in message and CONSTS["jim"]["user"] in message:

            contacts = self.db_inst.read_contacts(message[CONSTS["jim"]["user"]][CONSTS["jim"]["account"]])
            self.sendMsg(client, {CONSTS["jim"]["keys"]["responce"]: 202, "alert": contacts})
            return
        # добавляем контакт
        elif CONSTS["jim"]["action"] in message and \
            message[CONSTS["jim"]["action"]] == CONSTS["jim"]["keys"]["add_contact"] and \
            CONSTS["jim"]["time"] in message and CONSTS["jim"]["user"] in message:
            owner_ = message[CONSTS["jim"]["user"]][CONSTS["jim"]["account"]]
            client_ = message[CONSTS["jim"]["account"]]
            print(f"adding contact {owner_}->{client_}")
            error = self.db_inst.add_contact(owner_, client_)
            if error == "no owner":
                response = RESPONCES["resp_400"]
                response[CONSTS["jim"]["keys"]["error"]] = 'что-то пошло не так c вашим аккаунтом'
            elif error == "no owner":
                response = RESPONCES["resp_400"]
                response[CONSTS["jim"]["keys"]["error"]] = 'Не могу найти логин юзера для добавления'
            else:
                self.sendMsg(client, {CONSTS["jim"]["keys"]["responce"]: 200})
            return
        # удаляем контакт
        elif CONSTS["jim"]["action"] in message and \
            message[CONSTS["jim"]["action"]] == CONSTS["jim"]["keys"]["del_contact"] and \
            CONSTS["jim"]["time"] in message and CONSTS["jim"]["user"] in message:

            error = self.db_inst.del_contact(message[CONSTS["jim"]["user"]][CONSTS["jim"]["account"]], message[CONSTS["jim"]["account"]])
            if error == "no owner":
                response = RESPONCES["resp_400"]
                response[CONSTS["jim"]["keys"]["error"]] = 'что-то пошло не так c вашим аккаунтом'
            elif error == "no owner":
                response = RESPONCES["resp_400"]
                response[CONSTS["jim"]["keys"]["error"]] = 'Не могу найти логин юзера для удаления'
            else:
                self.sendMsg(client, {CONSTS["jim"]["keys"]["responce"]: 200})
            return
        # кладем в базу аватар, ответ не нужен
        elif CONSTS["jim"]["action"] in message and \
            message[CONSTS["jim"]["action"]] == CONSTS["jim"]["keys"]["add_avatar"] and \
            CONSTS["jim"]["time"] in message and CONSTS["jim"]["user"] in message:

            print("putting avatar in db")
            avatar = message[CONSTS["jim"]["keys"]["data"]]            
            owner_ = message[CONSTS["jim"]["user"]]
            print(owner_)
            print(avatar)
            print("==============================================")

            self.db_inst.add_avatar(owner_, base64.b64decode(avatar.encode(CONSTS['encoding'])))
            print("==============================================")

        # возвращаем аватар
        elif CONSTS["jim"]["action"] in message and \
            message[CONSTS["jim"]["action"]] == CONSTS["jim"]["keys"]["get_avatar"] and \
            CONSTS["jim"]["time"] in message and CONSTS["jim"]["user"] in message:

            owner_ = message[CONSTS["jim"]["user"]][CONSTS["jim"]["account"]]

            avatar = self.db_inst.get_avatar(owner_)
            avatar_ = base64.b64encode(avatar).decode(CONSTS["encoding"])
            self.sendMsg(client, {CONSTS["jim"]["keys"]["responce"]: 203, "alert": avatar_})

        # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
        elif CONSTS["jim"]["action"] in message and \
            message[CONSTS["jim"]["action"]] == CONSTS["jim"]["keys"]["message"] and \
            CONSTS["jim"]["destination"] in message and \
            CONSTS["jim"]["time"] in message and \
            CONSTS["jim"]["keys"]["message_text"] in message:
            print("new message")
            owner_ = message[CONSTS["jim"]["sender"]]
            client_ = message[CONSTS["jim"]["destination"]]
            self.messages_list.append(message)
            print(self.messages_list)
            return
        elif CONSTS["jim"]["action"] in message and \
            message[CONSTS["jim"]["action"]] == CONSTS["jim"]["keys"]["exit"] and \
            CONSTS["jim"]["account"] in message:            
            self.clients.remove(self.names[message[CONSTS["jim"]["account"]]])
            self.names[message[CONSTS["jim"]["account"]]].close()
            del self.names[message[CONSTS["jim"]["account"]]]
            return
        # Иначе отдаём Bad request
        else:
            response = RESPONCES["resp_400"]
            response[CONSTS["jim"]["keys"]["error"]] = 'Запрос некорректен.'
            self.sendMsg(client, message)
            return
        print("-------------------------------------------------")

    @LogDecorator()
    def processMsg(self, message):
        """отправка сообщения определенному пользователю"""
        print("отправка сообщения")
        print(message)
        if message[CONSTS["jim"]["destination"]] in self.names and \
            self.names[message[CONSTS["jim"]["destination"]]] in self.send_data_lst:
            self.sendMsg( self.names[message[CONSTS["jim"]["destination"]]], message)
        elif message[CONSTS["jim"]["destination"]] in self.names and \
            self.names[message[CONSTS["jim"]["destination"]]] not in self.send_data_lst:
            raise ConnectionError
        else:
            print("что-то пошло не так")
            pass
        print("----------------------------------------")

    @LogDecorator()
    def authorize(self, message, client):
        """ упрощенная авторизация 
            пока просто сверка хэшей
        """
        print("authorization")
        uName = message[CONSTS["jim"]["user"]][CONSTS["jim"]["account"]]
        # passHash = message[CONSTS["jim"]["user"]][CONSTS["jim"]["passhash"]]
        print(uName)
        if uName in self.names.keys():
            response = RESPONCES["resp_400"]
            response[CONSTS["jim"]["keys"]["error"]] = 'Имя пользователя уже занято.'
            try:
                self.sendMsg(client, response)
            except OSError:
                pass
            self.clients.remove(client)
            client.close()
            return
        elif not self.db_inst.check_user(uName):
            response = RESPONCES["resp_400"]
            response[CONSTS["jim"]["keys"]["error"]] = 'Пользователь не зарегистрирован'
            try:
                self.sendMsg(client, response)
            except OSError:
                pass
            # self.clients.remove(client)
            # client.close()
        else:
            # user_ = self.db_inst.check_user(uName)
            # if user_.userPassHash == passHash:
            #     self.sendMsg(client, {CONSTS["jim"]["keys"]["responce"]: 200})
            #     ip, port = client.getpeername()
            #     self.db_inst.user_login(uName, ip, port, None)
            #     self.names[uName] = client
            response_auth = RESPONCES["resp_511"]
            random_str = binascii.hexlify(os.urandom(64))
            response_auth[CONSTS["jim"]["keys"]["data"]] = random_str.decode('ascii')
            print(response_auth)
            hash_ = hmac.new(self.db_inst.get_hash(uName).encode(), random_str)
            digest = hash_.digest()
            # try:
                # Обмен с клиентом
            self.sendMsg(client, response_auth)
            ans = self.getMsg(client)
            print(f"ans: {ans}")
            # except OSError:
            #     client.close()
            #     return
            client_digest = binascii.a2b_base64(ans[CONSTS["jim"]["keys"]["data"]])
            if CONSTS["jim"]["keys"]["responce"] in ans and \
                ans[CONSTS["jim"]["keys"]["responce"]] == 511 and \
                hmac.compare_digest(digest, client_digest):
                print("here")
                self.names[uName] = client
                ip, port = client.getpeername()
                print(ip, port)
                self.db_inst.user_login(uName, ip, port, 
                    message[CONSTS["jim"]["user"]][CONSTS["jim"]["pubkey"]])
                self.sendMsg(client, RESPONCES["resp_200"])
                print("end")
            else:
                response = RESPONCES["resp_400"]
                response[CONSTS["jim"]["keys"]["error"]] = 'Пароли не совпадают'
                try:
                    self.sendMsg(client, response)
                except OSError:
                    pass
                self.clients.remove(client)
                client.close()

    @LogDecorator()
    def registration(self, message, client):
        """ регистрация """
        # пока пароль будет передаваться в виде хэша без дополнительного шифрования
        print("registration:")
        print(message)
        print(client)
        print("------------------------------------------------------")
        uName = message[CONSTS["jim"]["user"]][CONSTS["jim"]["account"]]
        passHash = message[CONSTS["jim"]["user"]][CONSTS["jim"]["passhash"]]
        self.db_inst.new_user(uName, passHash)
        self.sendMsg(client, {CONSTS["jim"]["keys"]["responce"]: 200})

    @LogDecorator()
    def runServer(self):
        print("running server")
        while True:
            try:
                # Принять запрос на соединение
                client, addr = self.socket.accept()
            except OSError:
                pass
            else:
                print(f"запрос на соединение от {str(addr)}")
                self.clients.append(client)
                print("------------------------------------------")
            finally:
                self.recv_data_lst = []
                self.send_data_lst = []
                self.err_lst = []     
                try:
                    if self.clients:
                        self.recv_data_lst, self.send_data_lst, self.err_lst = select.select(self.clients,
                                                                                             self.clients, 
                                                                                             [], 
                                                                                             0
                                                                                            )
                except:
                    pass

            if self.recv_data_lst:
                for client_with_message in self.recv_data_lst:
                    # try:
                    self.process_client_msg(self.getMsg(client_with_message), client_with_message)
                    # except:
                        # print("except branch")
                        # print(f'Клиент {client_with_message.getpeername()} '
                        #         f'отключился от сервера.')
                        # self.clients.remove(client_with_message)

            for msg in self.messages_list:
                try:
                    self.processMsg(msg)
                except:
                    self.clients.remove(self.names[msg[CONSTS["jim"]["destination"]]])
                    del self.names[msg[CONSTS["jim"]["destination"]]]
            self.messages_list.clear()

if __name__ == "__main__":
    serverInst = Server(getPort(sys.argv))
    serverInst.runServer()