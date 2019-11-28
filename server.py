#Python Socket Server
from socket import *
import select

class Server(object):
    def __init__(self):
        self._IP = "localhost"
        self._PORT = 1234
        self._serverSocket = (AF_INET, SOCK_STREAM)
	    
    def serverLoop(self):
        pass

server = Server()
