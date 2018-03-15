import threading
from socket import *

class FTPThread(threading.Thread):
    def __init__(self,threadID,connectionSocket):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.connectionSocket = connectionSocket
        self.quitting = False
        
    def run(self):
        while self.quitting == False:
            self.input = self.connectionSocket.recv(1024)
            self.CommandResolve(self.input)
            print("Closed Thread")
            
    def CheckUserName(self,username):
        userData = open("LoginDetails.txt",'r')
        users = userData.readlines()
        for x in range(0,users.__len__()):
            nameAndPass = users[x].split()
            if nameAndPass[0]==username:
                self.currentUsername = username
                self.currentUserPassword = nameAndPass[1]
                print "User Found"
                
    def CheckPassword(self,password):
        if password == self.currentUserPassword:
            print "Authenticated"
        else:
            print "Incorrect Password"

    def Port(self,port):
        self.portNumber = port
        
    def Retrieve(self,p):
        print p
        
    def Store(self,p):
        print p
        
    def OkServer(self):
        print "OK Server"
        
    def Quit(self):
        self.quitting = True
    
    commands = {
            "USER": lambda self: self.CheckUserName(self.parameter),
            "PASS": lambda self: self.CheckPassword(self.parameter),
            "PORT": lambda self: self.Port(self.parameter),
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
        except KeyError:
            print "Invalid Command" 


thread = FTPThread(1,1000)
#thread.start() Uncomment when the thread must recieve continuously
thread.CommandResolve("USER Tev")
thread.CommandResolve("PASS Pass1")