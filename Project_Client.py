from socket import *
import os

class ServerNotResponding(Exception):
    pass
class ResponseNotHandled(Exception):
    def __init__(self, response):
        self.response = response
        
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
        self.dataPort = Port - 1
        self.buffer = 4096
        self.parameter = ""
        reply = self.connectionSocket.recv(self.buffer)
        print reply
        if "220" not in reply:
            raise ServerNotResponding
              
        
    def RETR(self,fileAddress ,fileName): #still needs to replace download with file address
        self.CreatePassiveConnection()
        self.SendCommand("RETR " + fileName)
        reply = self.connectionSocket.recv(self.buffer)
                
        if reply[0]== "1":
            downloadData = self.dataSocket.recv(self.buffer)
            localFile = open(fileAddress + "\\" + fileName, "wb")
            while downloadData:
                localFile.write(downloadData)
                downloadData = self.dataSocket.recv(self.buffer)
                print downloadData
            localFile.close()
            reply = self.connectionSocket.recv(self.buffer)
            print reply
        elif "550" in reply:
            raise DoesntExist(fileName)
        elif "530" in reply:
            raise LoginError
        else:
            raise ResponseNotHandled(reply[0]+reply[1]+reply[2])
            
    def Login(self, username, password):
        self.SendCommand("USER " + username)
        reply = self.connectionSocket.recv(self.buffer)
        if "331" in reply:
            self.SendCommand("PASS " + password)
            reply = self.connectionSocket.recv(self.buffer)
            if "230" in reply:
                return
            else:
                raise LoginError
        else:
            raise LoginError
            
    def Port(self,port): 
        self.SendCommand(port)
        values = port.split(',')
        reply = self.connectionSocket.recv(self.buffer)
        if "200" in reply:
            self.dataPort = (int(values[4]) * 256) + int(values[5])
        else:
            raise PortChangeFailed
            
    def List(self, directory): #needs to default to None as per RFC
        if directory is not None:
            self.SendCommand("LIST " + directory)
        else:
            self.SendCommand("LIST")
        reply = self.connectionSocket.recv(self.buffer)
        if reply[0]== "1":
            self.CreatePassiveConnection()
            dirList = self.dataSocket.recv(self.buffer)
            return dirList
        elif "550" in reply:
            raise DoesntExist(directory)
        else:
            raise ResponseNotHandled(reply[0]+reply[1]+reply[2])
        
    def NList(self, directory): #needs to default to None as per RFC
        self.CreatePassiveConnection()
        if directory is not None:
            self.SendCommand("NLST " + directory)
        else:
            self.SendCommand("NLST")
        reply = self.connectionSocket.recv(self.buffer)
        if reply[0]== "1":
            dirList = self.dataSocket.recv(self.buffer)
            return dirList
        elif "550" in reply:
            raise DoesntExist(directory)
        else:
            raise ResponseNotHandled(reply[0]+reply[1]+reply[2])
    
    def STOR(self,fileAddress): 
        AddressParts = fileAddress.split("\\")
        fileName = AddressParts[-1]
        self.CreatePassiveConnection()
        self.SendCommand("STOR " + fileName)
        reply = self.connectionSocket.recv(self.buffer)
        fileExists = False
        fileAddressOnly = fileAddress.replace(fileName,"")
        
        if reply[0]== "1":
            for tempFileName in os.listdir(fileAddressOnly):
                if (tempFileName == fileName): 
                    fileExists = True
                    break
    
            if fileExists:
                localFile = open(fileAddress,"rb")
                uploadData = localFile.read(self.buffer)
                while uploadData:
                    self.dataSocket.send(uploadData)
                    uploadData= localFile.read(self.buffer)
                localFile.close()
            else:
                raise DoesntExist(fileName)
        elif "550" in reply:
            raise AccessDenied
        elif "530" in reply:
            raise LoginError
        else:
            raise ResponseNotHandled(reply[0]+reply[1]+reply[2])

    def SendCommand(self,message) :
        self.connectionSocket.send(message + "\r\n")
        
    def CreatePassiveConnection(self):
        self.SendCommand("PASV")
        reply = self.connectionSocket.recv(self.buffer)
        reply = reply.split(",")
        if reply[0].__len__() > 3:
            reply[0]= reply[0].split("(")[1]
        reply[len(reply)-1] = reply[len(reply)-1].split(")")[0]
        print reply
        self.dataIpAddress = reply[0]+"." + reply[1] + "." + reply[2]+ "." + reply[3]
        print self.dataIpAddress
        self.dataPort = int(reply[4])*256 + int(reply[5])
        print self.dataPort
        self.dataSocket = socket(AF_INET, SOCK_STREAM)
        self.dataSocket.connect((self.dataIpAddress, self.dataPort))
        
    def Quit(self):
        self.SendCommand("QUIT")
        reply = self.connectionSocket.recv(self.buffer)
        if "221" in reply:
            self.connectionSocket.close()
        #else:
          #  raise QuitError
            

