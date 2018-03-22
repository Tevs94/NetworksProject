from socket import *
import os
from FTPThread import FTPThread

publicSocket = socket(AF_INET, SOCK_STREAM)
publicSocket.bind(('', 3333)) #Initial socket
publicSocket.listen(10) #1 queued connection request allowed

print('Server online...')
privateSocket, clientAdress = publicSocket.accept() #accept handshake request, create dedicateds socket for client and finish handshake
thread = FTPThread(1,privateSocket)
thread.start()


'''
print clientAdress
fileName = 'temp'
fileExists = False

while (fileName != 'exit'):
    print "here"
    fileName = privateSocket.recv(4096)
    if(fileName != "temp"):
        for tempFileName in os.listdir("C:\Users\KittyBot\Documents\Networt_Project_S\Project_Server\client"):
            if (tempFileName == fileName):
                fileExists = True
                break
        print os.listdir("C:\Users\KittyBot\Documents\Networt_Project_S\Project_Server\client")
        if fileExists:
            localFile = open("client/" + fileName,"rb")
            uploadData = localFile.read(4096)
            while uploadData:
                print "dataISISISI: " + uploadData
                privateSocket.send(uploadData)
                uploadData= localFile.read(4096)
            privateSocket.close()
            localFile.close()
            print "sent file"
        else:
            privateSocket.send("550")

        

privateSocket.close()
publicSocket.close()
'''