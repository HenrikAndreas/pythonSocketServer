# Server Class
# if their client is not identical to mine -- refuse access
# Read from log and send to users
from socket import *
import sys
import select
from datetime import datetime

class Server(object):
    def __init__(self):
        # self._IP = "10.0.0.119"
        self._IP = "localhost"
        self._PORT = 1234
        self._messageLength = 150
        self._serverSocket = socket(AF_INET, SOCK_STREAM)
        self._serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._serverSocket.bind((self._IP, self._PORT))
        self._serverSocket.listen()
        self._socketsList = [self._serverSocket]
        self._clients = {} #clientSocket : username
        self._time = f"{datetime.now().year}:{datetime.now().month}:{datetime.now().day} {datetime.now().hour}.{datetime.now().minute}"
        self._users = self._getUsers()

        serverMsg = f'{self._time}: Listening on {self._IP}:{self._PORT}...'
        self.log(serverMsg)
        print(serverMsg)

    # Updating self._time variable
    def timeUpdate(self):
        self._time = f"{datetime.now().year}:{datetime.now().month}:{datetime.now().day} {datetime.now().hour}.{datetime.now().minute}"
    # Initiating the dictionary that stores usernames and passwords
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
        
    # creating a new user | registering
    def newUser(self, username, password):
        dataFile = open("users.dat", 'a')
        dataFile.write(f"{username}       {password}\n")
        dataFile.close()
    # Logs all server activity
    def log(self, message):
        logFile = open('log.dat', 'a')
        logFile.write(f'{message}\n')
        logFile.close()

    # Writes out history in clients terminal, so that client can view previous messages
    def writeToHistory(self, message):
        historyFile = open('chatHistory.dat', 'a')
        historyFile.write(f"{message}\n")
        historyFile.close()

    def sendHistory(self, client):
        historyFile = open('chatHistory.dat', 'r')
        client.send('Previous messages\n-------------'.encode('utf-8'))
        for line in historyFile:
            client.send(line.encode('utf-8'))
        historyFile.close()
        client.send(('-' * 15).encode('utf-8'))
    
    def getIP(self):
        return self._IP

    def getPort(self):
        return self._PORT

    def removeSocket(self, socket):
        serverMsg = f"{self._time}: {self._clients[socket]} disconnected"
        self.log(serverMsg)
        print(serverMsg)
        # Sending disconnect to all clients
        for client in self._clients:
            if client != socket:
                client.send(f"{self._clients[socket]} disconnected".encode('utf-8'))
        self._socketsList.remove(socket)
        del self._clients[socket]



    def serverLoop(self):
        while True:
            readSockets, writeSockets, exceptionSockets = select.select(self._socketsList, [], self._socketsList)
            self.timeUpdate() # Get correct time

            for notifiedSocket in readSockets:

                # Accept new connection...
                if notifiedSocket == self._serverSocket:
                    clientSocket, clientAddress = self._serverSocket.accept()
                    
                    username = clientSocket.recv(self._messageLength).decode('utf-8')
                    # If username exists - login
                    if username in self._users:
                        clientSocket.send('Enter password: '.encode('utf-8'))

                        loginPassword = clientSocket.recv(self._messageLength)
                        loginPassword = loginPassword.decode('utf-8')
                        if loginPassword == self._users[username]:
                            clientSocket.send(f'Welcome {username}!\n'.encode('utf-8'))
                
                        else:
                            clientSocket.send("Wrong password\n> Disconnected".encode('utf-8'))
                            clientSocket.close()
                            continue

                    # If username doesn't exist - register
                    else:
                        clientSocket.send('Not found. Create new account? (y / n)'.encode('utf-8'))
                        answer = clientSocket.recv(self._messageLength).decode('utf-8').lower()
                        if answer == 'y':

                            clientSocket.send("Enter username: ".encode('utf-8'))
                            username = clientSocket.recv(self._messageLength).decode('utf-8').lower()

                            if (len(username.split()) > 1):
                                clientSocket.send(f"Username cannot consist of more than one word\n> Disconnected".encode('utf-8'))
                                clientSocket.close()
                                continue

                            if  (len(username) > self._messageLength):
                                clientSocket.send(f"Username cannot exceed {self._messageLength} characters\n> Disconnected".encode('utf-8'))
                                clientSocket.close()
                                continue
                                
                            

                            clientSocket.send("Enter password: ".encode('utf-8'))
                            password = clientSocket.recv(self._messageLength).decode('utf-8')
                            if (len(password.split()) > 1):
                                clientSocket.send(f"Password cannot consist of more than one word\n> Disconnected".encode('utf-8'))
                                clientSocket.close()
                                continue
                            
                            self.newUser(username, password)
                            # Updating our database without closing server
                            self._users = self._getUsers()
                        else:
                            clientSocket.send("> Disconnected ".encode('utf-8'))
                            clientSocket.close()
                            continue
                    # If we succeded to login, place client in our socketList for select
                    # and set clientSocket in dict with username as value. Also we send the client
                    # the chat history
                    self.sendHistory(clientSocket)

                    self._clients[clientSocket] = username
                    self._socketsList.append(clientSocket)
                    
                    serverMsg = f"{self._time}: {self._clients[clientSocket]} on {clientAddress[0]}:{clientAddress[1]} connected"
                    self.log(serverMsg)
                    print(serverMsg)
                    
                    # Send message to all clients who has connected
                    for client in self._clients:
                        client.send(f"{self._clients[clientSocket]} connected".encode('utf-8'))

                # Connection exists > New message is recieved
                else:

                    try:
                        
                        message = notifiedSocket.recv(self._messageLength)
                        
                        if not message or message == False:
                            self.removeSocket(notifiedSocket)
                            continue

                    # Client suddenly disconnected
                    except ConnectionResetError:
                        self.removeSocket(notifiedSocket)
                        continue
                    
                    
                    serverMsg = f"{self._time}: Recieved message from {self._clients[notifiedSocket]}: {message.decode('utf-8')}"
                    self.log(serverMsg)
                    print(serverMsg)

                    fullMessage = f"{self._clients[notifiedSocket]} >>> {message.decode('utf-8')}"
                    self.writeToHistory(fullMessage)
                    # send message to all clients apart from the source
                    for client in self._clients:
                        if client != notifiedSocket:
                            client.send(fullMessage.encode('utf-8'))



server = Server()
server.serverLoop()
