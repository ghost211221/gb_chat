import unittest
import time
from socket import *
import json

import sys
sys.path.append("..")

from subprocess import Popen, PIPE

from server import Server

class TestServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def setUp(self):
        # настраиваем сервер
        self.ServerUUT = Popen("python ..\\server.py 7777", stdout=PIPE)
        # настраиваем клиент
        self.Client = socket(AF_INET, SOCK_STREAM)
        self.Client.connect(("127.0.0.1", 7777))

    def test_communication_success(self):
        msg = {
           "action":"presence",
            "time": time.time(),
            "user": {
                "account_name": "Guest"
            }
        }
        self.Client.send(json.dumps(msg).encode("utf8"))        
        responce = json.loads(self.Client.recv(1024).decode("utf8"))
        self.assertEqual(responce, {"responce": 200})


    def test_communication_400(self):
        msg = {
           "action":"presence",
            # "time": time.time(),
            "user": {
                "account_name": "Guest"
            }
        }
        self.Client.send(json.dumps(msg).encode("utf8"))        
        responce = json.loads(self.Client.recv(1024).decode("utf8"))
        self.assertEqual(responce, {"responce_default_adress": 400, "error": 'Bad Request'})

    def tearDown(self):
        self.ServerUUT.terminate()
        self.Client.close()

    @classmethod
    def tearDownClass(self):
        try:            
            self.ServerUUT.terminate()
            self.Client.close()
        except:
            pass

if __name__ == "__main__":
    unittest.main(verbosity=3)