# Server Class
# if their client is not identical to mine -- refuse access
from socket import *
import sys
import select

class Server(object):
    def __init__(self):
        self._IP = "localhost"
        self._PORT = 1234
        self._messageLength = 1024
        self._serverSocket = socket(AF_INET, SOCK_STREAM)
        self._serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._serverSocket.bind((self._IP, self._PORT))
        self._serverSocket.listen()
        self._socketsList = [self._serverSocket]
        self._clients = {} #clientSocket : username

        self._users = {'henrik' : '123!', 'bodil' : 'henrik123'}
        print(f'Listening on {self._IP}:{self._PORT}...')
        

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
                    
                    username = clientSocket.recv(self._messageLength).decode('utf-8')
                    if username in self._users:
                        clientSocket.send('Enter password: '.encode('utf-8'))

                        loginPassword = clientSocket.recv(self._messageLength)
                        loginPassword = loginPassword.decode('utf-8')
                        if loginPassword == self._users[username]:
                            clientSocket.send(f'Welcome {username}!'.encode('utf-8'))
                        else:
                            clientSocket.send("Wrong password".encode('utf-8'))

                    else:
                        clientSocket.send('Not found. Create new account? (y / n)'.encode('utf-8'))

                    self._clients[clientSocket] = username
                    self._socketsList.append(clientSocket)
                    
                    print(f"{self._clients[clientSocket]} on {clientAddress[0]}:{clientAddress[1]} connected")
                
                else:
                    message = notifiedSocket.recv(self._messageLength)
                    
                    if not message:
                        print(f'{self._clients[notifiedSocket]} disconnected')
                        self._socketsList.remove(notifiedSocket)
                        del self._clients[notifiedSocket]
                        
                        continue

                    
                    print(f"Recieved message from {self._clients[notifiedSocket]}: {message.decode('utf-8')}")

                    fullMessage = f"{self._clients[notifiedSocket]} >>> {message.decode('utf-8')}"

                    for client in self._clients:
                        if client != notifiedSocket:
                            client.send(fullMessage.encode('utf-8'))




                    

                    
server = Server()
server.serverLoop()
