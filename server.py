# Server Class
# if their client is not identical to mine -- refuse access
# create possibility to register
from socket import *
import sys
import select

class Server(object):
    def __init__(self):
        self._IP = "10.0.0.63"
        self._PORT = 1234
        self._messageLength = 1024
        self._serverSocket = socket(AF_INET, SOCK_STREAM)
        self._serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._serverSocket.bind((self._IP, self._PORT))
        self._serverSocket.listen()
        self._socketsList = [self._serverSocket]
        self._clients = {} #clientSocket : username

        self._users = self._getUsers()

        print(f'Listening on {self._IP}:{self._PORT}...')
        
    def _getUsers(self):
        users = {}
        dataFile = open("users.dat", 'r')

        line = dataFile.readline()
        while line != "":
            line = line.split()
            users[line[0]] = line[1]
            line = dataFile.readline()

        dataFile.close()
        return users

    def newUser(self, username, password):
        dataFile = open("users.dat", 'a')
        dataFile.write(f"{username}       {password}\n")
        dataFile.close()
        

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
                            clientSocket.close()
                            continue


                    else:
                        clientSocket.send('Not found. Create new account? (y / n)'.encode('utf-8'))
                        answer = clientSocket.recv(self._messageLength).decode('utf-8').lower()
                        if answer == 'y':
                            clientSocket.send("Enter username: ".encode('utf-8'))
                            username = clientSocket.recv(self._messageLength).decode('utf-8').lower()
                            print(f'New: {username}')

                            clientSocket.send("Enter password: ".encode('utf-8'))
                            password = clientSocket.recv(self._messageLength).decode('utf-8')

                            self.newUser(username, password)
                            # Updating our database without closing server
                            self._users = self._getUsers()
                        else:

                            clientSocket.close()
                            continue

                    self._clients[clientSocket] = username
                    self._socketsList.append(clientSocket)
                    
                    print(f"{self._clients[clientSocket]} on {clientAddress[0]}:{clientAddress[1]} connected")
                    
                    for client in self._clients:
                        client.send(f"{self._clients[clientSocket]} connected".encode('utf-8'))
                       


                # Connection exists > New message is recieved
                else:
                    message = notifiedSocket.recv(self._messageLength)
                    
                    if not message:
                        print(f'{self._clients[notifiedSocket]} disconnected')
                        # Sending disconnect to all clients
                        for client in self._clients:
                            if client != notifiedSocket:
                                client.send(f"{self._clients[notifiedSocket]} disconnected".encode('utf-8'))
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
