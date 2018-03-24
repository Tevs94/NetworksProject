from socket import *
import os

class ServerNotResponding(Exception):
    pass

class LoginError(Exception):
    pass

class DoesntExist(Exception):
    def __init__(self, fileName):
        self.fileName = fileName

class BadConnection(Exception):
    pass

class PortChangeFailed(Exception):
    pass

class AccessDenied(Exception):
    pass
class QuitError(Exception):
    pass

class ClientHandler():
    def __init__(self, IP_Address, Port):
        self.connectionSocket = socket(AF_INET, SOCK_STREAM) #Set IPv4 and TCP
        self.connectionSocket.connect((IP_Address, Port)) #Intial handshake call to set up connection
        self.dataPort = 10000
        self.buffer = 4096
        self.parameter = ""
        reply = self.connectionSocket.recv(self.buffer)
        if "220" not in reply:
            raise ServerNotResponding
              
        
    def RETR(self,fileAddress ,fileName): #still needs to replace download with file address
        self.connectionSocket.send("RETR " + fileName)
        reply = self.connectionSocket.recv(self.buffer)
        
        if "150" in reply:
            recieveSocket = self.EstablishConnection()
            downloadData = recieveSocket.recv(self.buffer)
            localFile = open("./Downloads/" + fileName, "wb")
            while downloadData:
                localFile.write(downloadData)
                downloadData = recieveSocket.recv(self.buffer)
            reply = self.connectionSocket.recv(self.buffer)
            localFile.close()
            print downloadData
        elif "550" in reply:
            raise DoesntExist(fileName)
        elif "530" in reply:
            raise LoginError
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
        self.connectionSocket.send(port)
        values = port.split(',')
        reply = self.connectionSocket.recv(self.buffer)
        if "200" in reply:
            self.dataPort = (int(values[4]) * 256) + int(values[5])
        else:
            raise PortChangeFailed
            
    def List(self, directory): #needs to default to None as per RFC
        self.connectionSocket.send("LIST " + directory)
        reply = self.connectionSocket.recv(self.buffer)
        if "150" in reply:
            dataConnection = self.EstablishConnection()
            dirList = dataConnection.recv(self.buffer)
            return dirList
        elif "550" in reply:
            raise DoesntExist(directory)
        else:
            raise LoginError
        
    def STOR(self,fileAddress): 
        self.connectionSocket.send("STOR " + fileAddress)
        reply = self.connectionSocket.recv(self.buffer)
        fileExists = False
        filename = ""
        if "150" in reply:
            for tempFileName in os.listdir(fileAddress + fileName):
                if (tempFileName == fileName): 
                    fileExists = True
                    dataSocket = self.EstablishConnection()
                    break
    
            if fileExists:
                localFile = open(fileAddress + "/" + fileName,"rb")
                uploadData = localFile.read(self.buffer)
                while uploadData:
                    dataSocket.send(uploadData)
                    uploadData= localFile.read(self.buffer)
                localFile.close()
            else:
                raise DoesntExist(fileName)
        elif "550" in reply:
            raise AccessDenied
        else:
            raise LoginError
        
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
         
    def EstablishConnection(self):
        dataSocket = socket(AF_INET, SOCK_STREAM)
        dataSocket.bind(('', self.dataPort))
        dataSocket.listen(1) 
        recieveSocket, clientAddress = dataSocket.accept()
        return recieveSocket
    
    def Quit(self):
        self.connectionSocket.send("QUIT")
        reply = self.connectionSocket.recv(self.buffer)
        if "221" in reply:
            self.connectionSocket.close()
        #else:
          #  raise QuitError
            

