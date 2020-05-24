from sys import argv, path, _getframe
import socket
path.append('../')

class LoginRequired():
    def __call__(self, func):
        def decorated(*args, **kwargs):
            # импорт работает только тут
            from server import Server
            from utils.variables import CONSTS
            print("=================== DECORATOR ======================")
            print(args[0].names)
            print(args[0].clients)
            print("=================== ENDDECORATOR ===================")
            if isinstance(args[0], Server):
                found = False
                for arg in args:
                    if isinstance(arg, socket.socket):
                        for client in args[0].clients:
                            if client == arg:
                                found = True

                for arg in args:
                    if isinstance(arg, dict):
                        if CONSTS["jim"]["action"] in arg and \
                            arg[CONSTS["jim"]["action"]] == CONSTS["jim"]["keys"]["presence"]:

                            found = True

                if not found:
                    raise TypeError

            return func(*args, **kwargs)
        return decorated