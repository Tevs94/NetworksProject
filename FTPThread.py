import threading
import os
from socket import *

class FTPThread(threading.Thread):
    def __init__(self,threadID,connectionSocket):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.connectionSocket = connectionSocket
        self.quitting = False
        self.SendReply(220)
        self.loggedIn = False
        
    def run(self):
        while self.quitting == False:
            self.input = self.connectionSocket.recv(1024)
            self.CommandResolve(self.input)
            
        self.SendReply(226)
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
            self.userFolder = "/Users/" + self.currentUsername
            print "Authenticated"
        else:
            self.SendReply(530)
            print "Incorrect Password"
    
    def Port(self,port):
        self.portNumber = port
        self.SendReply(200)
    
    def List(self):
        if self.loggedIn:
            self.SendReply(150)
            dirList = os.listdir('./Users/'+self.currentUsername)
            print dirList
        else:
            self.SendReply(530)  
            
    def Retrieve(self,p):
        self.SendReply(200)
        self.SendReply(250)
        print p
        
    def Store(self,p):
        self.SendReply(200)
        self.SendReply(250)
        print p
        
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
            commandParameter = ""
        else:
            commandParameter = command[1]
        try:
            self.parameter = commandParameter
            self.commands.get(commandCode)(self)
        except (KeyError, TypeError):
            self.SendReply(500)
            print "Invalid Command" 
        
            
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
        message = self.replies.get(code)(self)
        self.connectionSocket.send(message)


thread = FTPThread(1,1000)
#thread.start() Uncomment when the thread must recieve continuously
thread.CommandResolve("USER Tev")
thread.CommandResolve("PASS Pass1")
thread.CommandResolve("LIST")
