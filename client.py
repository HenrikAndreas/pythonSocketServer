from socket import *
import threading
import sys
import errno

class Client(object):
    def __init__(self):
        self._IP = "localhost"
        self._PORT = 1234
        self._HEADERLENGTH = 1024
        self._username = input("Enter username: ")
        self._clientSocket = socket(AF_INET, SOCK_STREAM)
        self._clientSocket.connect((self._IP, self._PORT))
        self._clientSocket.setblocking(False)
        self._myUsername = self._username.encode('utf-8')
        self._clientSocket.send(self._myUsername)






client = Client()