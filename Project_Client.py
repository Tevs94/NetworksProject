from socket import *

clientSocket = socket(AF_INET, SOCK_STREAM) #Set IPv4 and TCP
clientSocket.connect(('localhost', 3333)) #Intial handshake call to set up connection
fileName = "temp"

while (fileName != 'exit'):
    fileName = raw_input('File Location/name:')
    clientSocket.send(fileName)
    #This controls the download process. 
    #Checks if data isnt finished transfering so continues until down.
    downloadData = clientSocket.recv(4096)
    
    if(downloadData != "550"):
        localFile = open("downloads/"+fileName, "wb")
        while downloadData:
            print "dataISISISI: " + downloadData
            localFile.write(downloadData)
            downloadData = clientSocket.recv(4096)
        localFile.close()
        print "Finished"
    else:
        print "No file of name " + fileName

clientSocket.close()
