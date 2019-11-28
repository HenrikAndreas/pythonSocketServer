from socket import *
import sys
import select

class Server(object):
    def __init__(self):
        self._IP = "localhost"
        self._PORT = 1234
        self._HEADERLENGTH = 1024
        self._serverSocket = socket(AF_INET, SOCK_STREAM)
        self._serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._serverSocket.bind((self._IP, self._PORT))
        self._serverSocket.listen()
        self._socketsList = [self._serverSocket]
        self._clients = {}
    
    def getIP(self):
        return self._IP

    def getPort(self):
        return self._PORT
    
    def _recieveMessage(self, clientSocket):
        pass

    def serverLoop(self):
        while True:
            readSockets, writeSockets, exceptionSockets = select.select(self._socketsList, [], self._socketsList)

            for notifiedSocket in readSockets:

                if notifiedSocket == self._serverSocket:
                    clientSocket, clientAdress = self._serverSocket.accept()
                    
                    username = clientSocket.recv(self._HEADERLENGTH)
                    print(username.decode('utf-8'))
                    password = None #FIX
                    
                    

                    
server = Server()
# server.serverLoop()