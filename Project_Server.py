from socket import *
from FTPThread import FTPThread

publicSocket = socket(AF_INET, SOCK_STREAM)
publicSocket.bind(('', 3333)) #Initial socket
publicSocket.listen(10) #1 queued connection request allowed

print('Server online...')
privateSocket, clientAddress = publicSocket.accept() #accept handshake request, create dedicateds socket for client and finish handshake
thread = FTPThread(1,privateSocket, 3333,clientAddress)
thread.start()