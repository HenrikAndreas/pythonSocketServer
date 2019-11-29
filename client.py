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

        inputThread = threading.Thread(target=self.messageSender)
        inputThread.daemon = True
        inputThread.start()
	
        while True:
            try:
                message = self._clientSocket.recv(self._HEADERLENGTH).decode('utf-8')
                if message != '' :
                    print(message)


            # If simply no message recieved, ignore error and start loop over
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print(f'Reading error: {str(e)}')
                    sys.exit()
                continue
        
    def messageSender(self):
        while True:
            message = input('')

            if message:
                message = message.encode('utf-8')
                self._clientSocket.send(message)
                #Send username with message
                #in server - associate clientsocket object with username and add to message


client = Client()
