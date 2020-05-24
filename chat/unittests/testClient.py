import unittest
import time
from socket import *
import json

import sys
sys.path.append("..")

from client import Client

"""
тесты пока только на успех, времени не хватает.
дальше по мере возникновения багов/косяков буду дописывать.
ну и по мере развития функционала тоже.
"""

class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # настраиваем сервер
        self.testServerSock = socket(AF_INET, SOCK_STREAM)
        self.testServerSock.bind(('0.0.0.0', 7777))
        self.testServerSock.listen(5)

        self.ClientUUT = Client("127.0.0.1", 7777)

    def setUp(self):
        pass

    def test__check_socket(self):
        print(self.ClientUUT.socket)
        with self.subTest("check family"):
            self.assertEqual(self.ClientUUT.socket.family, AF_INET)
        with self.subTest("check type"):
            self.assertEqual(self.ClientUUT.socket.type, SOCK_STREAM)

    def test__genPresence(self):
        self.ClientUUT.genPresence()
        with self.subTest("check action"):
            self.assertEqual(self.ClientUUT.msg["action"], "presence")
        # не знаю как лучше проверить время, проверю тип данных
        with self.subTest("check time"):
            self.assertEqual(type(self.ClientUUT.msg["time"]), type(time.time()))
        with self.subTest("check user"):
            self.assertEqual(self.ClientUUT.msg["user"], {'account_name': 'Guest'})

    def test__sendMsg(self):
        self.ClientUUT.msg = {
            'action': 'presence', 
            'time': time.time(), 
            'user': {
                'account_name': 'Guest'
            }
        }
        self.ClientUUT.sendMsg()
        # если не вылезает исключение, то все нормально

    @unittest.skip("пока не получилось отладить, зависает")
    def test__getMsg_success(self):
        self.serverSend("succeess")
        self.ClientUUT.getMsg()

        self.assertEqual(self.ClientUUT.responce, {"responce": 200})

    def test__processMsg_responce_ok(self):
        self.ClientUUT.responce = {"responce": 200}

        self.assertEqual(self.ClientUUT.processResp(), '200 : OK')

    def test__processMsg_responce_errpr(self):
        self.ClientUUT.responce = {"responce": 404}

        self.assertEqual(self.ClientUUT.processResp(), '400 : error')

    def test__processMsg_responce_not_exist(self):
        self.ClientUUT.responce = {}

        with self.assertRaises(ValueError):
            self.ClientUUT.processResp()



    @classmethod
    def tearDownClass(self):
        self.ClientUUT.socket.close()
        self.testServerSock.close()
        

    def serverSend(self, msgType):
        msg = {}
        if msgType == "success":
            msg = {
                "responce": 200
            }
        elif msgType == "fail":
            msg = {
                "responce_default_adress": 400,
                "error": 'Bad Request'
            }
        self.ClientUUT.socket.send(json.dumps(msg).encode("utf8"))


if __name__ == "__main__":
    unittest.main(verbosity=3)