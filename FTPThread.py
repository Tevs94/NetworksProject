import threading
import os
from socket import *

class FTPThread(threading.Thread):
    def __init__(self,threadID,connectionSocket, portNum, clientAddress):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.dataportNumber = portNum + 1
        self.controlPort = clientAddress[1]
        self.clientIPAddress = clientAddress[0]
        self.dataIPAddress = self.clientIPAddress
        self.connectionSocket = connectionSocket
        self.quitting = False
        self.SendReply(220)
        self.buffer = 4096
        self.loggedIn = False
        
        
    def run(self):
        while self.quitting == False:
            self.input = self.connectionSocket.recv(1024)
            self.CommandResolve(self.input)
            
        self.SendReply(221)
        print("Closed Thread")
            
    def CheckUserName(self,username):
        userData = open("LoginDetails.txt",'r')
        users = userData.readlines()
        userFound = False
        for x in range(0,users.__len__()):
            nameAndPass = users[x].split()
            if nameAndPass[0]==username:
                self.currentUsername = username
                self.currentUserPassword = nameAndPass[1]
                self.SendReply(331)
                userFound = True
                print "User Found"
        if userFound == False:
            self.SendReply(530) 
            print "User Not found"
                
    def CheckPassword(self,password):
        if password == self.currentUserPassword:
            self.SendReply(230)
            self.loggedIn = True
            self.userFolder = "./Users/" + self.currentUsername + "/"
            print "Authenticated"
        else:
            self.SendReply(530)
            print "Incorrect Password"
    
    def Port(self,port):
        values = port.split(',')
        self.dataportNumber = (int(values[4]) * 256) + int(values[5])
        self.dataIPAddress = values[0] + '.' + values[1] + '.' + values[2] + '.' + values[3]
        self.SendReply(200)

    def Retrieve(self,fileName):
        if self.loggedIn:
            fileExists = False
            
            for tempFileName in os.listdir(self.userFolder):
                if (tempFileName == fileName): 
                    fileExists = True
                    self.SendReply(150)
                    self.CreateDataConnection()
                    break
    
            if fileExists:
                localFile = open(self.userFolder + fileName,"rb")
                uploadData = localFile.read(self.buffer)
                while uploadData:
                    self.dataSocket.send(uploadData)
                    uploadData= localFile.read(self.buffer)
                localFile.close()
                self.SendReply(226)
            else:
                self.SendReply(550)
        else:
            self.SendReply(530)  
    
    def List(self):
        if self.loggedIn:
            self.SendReply(150)
            if self.parameter is None:
                directory = ""
            else:
                directory = self.parameter
            
            if(os.path.isdir(self.userFolder + directory)):
                dirList = os.listdir(self.userFolder + directory)
                sendString = ", ".join(dirList)
                print sendString
                self.CreateDataConnection()
                self.dataSocket.send(sendString)
            else:
                self.SendReply(550)
        else:
            self.SendReply(530)  
              
    def Store(self, fileName):
        if self.loggedIn:
            self.SendReply(150)
            self.CreateDataConnection()
            downloadData = self.dataSocket.recv(self.buffer)
            localFile = open(self.userFolder + fileName, "wb")
            while downloadData:
                localFile.write(downloadData)
                downloadData = self.dataSocket.recv(self.buffer)
            self.SendReply(226)
            localFile.close()
            print downloadData
            #No idea why it would send an access denied
        else:
            self.SendReply(530) 
        
    def OkServer(self):
        print "OK Server"
        
    def Quit(self):
        self.SendReply(221)
        self.quitting = True
    
    commands = {
            "USER": lambda self: self.CheckUserName(self.parameter),
            "PASS": lambda self: self.CheckPassword(self.parameter),
            "PORT": lambda self: self.Port(self.parameter),
            "LIST": lambda self: self.List(),
            "RETR": lambda self: self.Retrieve(self.parameter),
            "STOR": lambda self: self.Store(self.parameter),
            "NOOP": lambda self: self.OkServer(),
            "QUIT": lambda self: self.Quit()
            }
     
    def CommandResolve(self,commandString):
        command = commandString.split()
        commandCode = command[0]
        if command.__len__() == 1:
            commandParameter = None
        else:
            commandParameter = command[1]
        try:
            self.parameter = commandParameter
            self.commands.get(commandCode)(self)
        except (KeyError, TypeError) as e:
            self.SendReply(500)
            print e
        
            
    replies = {
            150: "150 File status okay; about to open data connection.",
            200: "200 Command okay.",
            202: "202 Command not implemented, superfluous at this site.",
            220: "220 Service ready for new user",    
            221: "221 Service closing control connection. Logged out.",
            226:	"226 Closing data connection. Requested file action successful",
            230: "230 User logged in, proceed.",
            250: "250 Requested file action okay, completed.",
            331: "331 User name okay, need password.",
            425:	"425 Can't open data connection",
            500: "500 Syntax error, command unrecognized",
            530: "530 Not logged in or log in details incorrect",
            550: "550 Requested action not taken. File unavailable"
     
            }
    
    def SendReply(self, code):
        message = self.replies.get(code)
        self.connectionSocket.send(message)

    def CreateDataConnection(self):
        self.dataSocket = socket(AF_INET, SOCK_STREAM) #Set IPv4 and TCP
        self.dataSocket.connect((self.dataIPAddress, self.dataportNumber))
