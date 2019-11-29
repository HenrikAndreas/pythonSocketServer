# Server Class
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

        self._users = {'henrik' : '123!', 'bodil' : 'henrik123'}
        print('listening..')
        

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

                # Accept new connection...
                if notifiedSocket == self._serverSocket:
                    clientSocket, clientAddress = self._serverSocket.accept()
                    
                    username = clientSocket.recv(self._HEADERLENGTH).decode('utf-8')
                    if username in self._users:
                        clientSocket.send('Enter password: '.encode('utf-8'))
                        loginPassword = clientSocket.recv(self._HEADERLENGTH)
                        loginPassword = loginPassword.decode('utf-8')
                        if loginPassword == self._users[username]:
                            clientSocket.send(f'Velkommen {username}!'.encode('utf-8'))
                    else:
                        clientSocket.send('Not found. Create new account? (y / n)'.encode('utf-8'))
                    

                    

                    
server = Server()
server.serverLoop()
