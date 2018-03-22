from socket import *

class LoginError(Exception):
    pass

class FileDoesntExist(Exception):
    def __init__(self, fileName):
        self.fileName = fileName

class BadConnection(Exception):
    pass

class PortChangeFailed(Exception):
    pass

class ClientHandler():
    def __init__(self,connectionSocket):
        self.connectionSocket = connectionSocket
        self.dataPort = 10000
        self.buffer = 4096
        self.parameter = ""
        
    def RETR(self,fileAddress ,fileName):
        self.connectionSocket.send("RETR " + fileName)
        dataSocket = socket(AF_INET, SOCK_STREAM)
        dataSocket.bind(('', self.dataPort))
        dataSocket.listen(1) 
        recieveSocket, clientAddress = dataSocket.accept()
        downloadData = self.connectionSocket.recv(self.buffer)
        
        if "150" in downloadData:
            downloadData = self.recieveSocket.recv(self.buffer)
            localFile = open("./Downloads/" + fileName, "wb")
            while downloadData:
                localFile.write(downloadData)
                downloadData = self.recieveSocket.recv(self.buffer)
            downloadData = self.connectionSocket.recv(self.buffer)
            localFile.close()
            print downloadData
        elif "550" in downloadData:
            raise FileDoesntExist(fileName)
        else:
            raise BadConnection
            
    def Login(self, username, password):
        self.connectionSocket.send("USER " + username)
        reply = self.connectionSocket.recv(self.buffer)
        if "331" in reply:
            self.connectionSocket.send("PASS " + password)
            reply = self.connectionSocket.recv(self.buffer)
            if "230" in reply:
                return
            else:
                raise LoginError
        else:
            raise LoginError
            
    def Port(self,port): 
        self.connectionSocket.send("USER " + username)
        reply = self.connectionSocket.recv(self.buffer)
        if "200" in reply:
            self.dataPort = port
        else:
            raise PortChangeFailed
    
    def CommandResolve(self,commandString):
        command = commandString.split()
        commandCode = command[0]
        if command.__len__() == 1:
            commandParameter = ""
        else:
            commandParameter = command[1]
        try:
            self.parameter = commandParameter
            self.commands.get(commandCode)(self)
        except (KeyError, TypeError):
            print "Invalid Command" 
            
    def SendBasicMessage(self, message):
         self.connectionSocket.send(message)
