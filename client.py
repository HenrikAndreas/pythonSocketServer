# Add color to own message > Easier to distinguish
# If not login --> Sys.exit()
from socket import *
import threading
import sys
import errno

class Client(object):
    def __init__(self, username):
        self._IP = 'localhost'#"80.212.111.238"
        self._PORT = 1234
        self._messageLength = 150
        self._username = username
        self._clientSocket = socket(AF_INET, SOCK_STREAM)


    def clientLoop(self):
        # Setting up thread
        inputThread = threading.Thread(target=self.messageSender)
        inputThread.daemon = True
        inputThread.start()

        # Listening for messages
        while True:
            try:
                message = self._clientSocket.recv(self._messageLength).decode('utf-8')
                if message != '' :
                    print(message)

            # If simply no message recieved, ignore error and start loop over
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print(f'Reading error: {str(e)}')
                    sys.exit()
                continue

    # Thread to send messages
    def messageSender(self): 
        while True:
            message = input('')
            if message:
                message = message.encode('utf-8')
                self._clientSocket.send(message)

    def sendUsername(self):
        self._myUsername = self._username.encode('utf-8')
        self._clientSocket.send(self._myUsername)

    def connectToServer(self):
        self._clientSocket.connect((self._IP, self._PORT))
        self._clientSocket.setblocking(False)        


username = input('Enter username ')

client = Client(username)
client.connectToServer()
client.sendUsername()
client.clientLoop()
