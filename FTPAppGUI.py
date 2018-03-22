import Tkinter as tk
from enum import Enum

class FTPGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("FTP Application")
        # adapted from https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
        # and https://stackoverflow.com/questions/35991126/tkinter-frame-resize
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        self.frames = {}
        for F in (ChooseServer, Login, UploadDownload, Download, Upload):
            pageName = F.__name__
            frame = F(container, self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="NSEW")
    
        self.DisplayPage("ChooseServer")
                
    def DisplayPage(self,pageName):
        for frame in self.frames.values():
            frame.grid_remove()
            
        frame = self.frames[pageName]
        frame.grid()

       
class ChooseServer(tk.Frame):
    def __init__(self,window,controllerWindow):
        tk.Frame.__init__(self, window)
        self.window = window
        self.controllerWindow = controllerWindow
        
        self.titleLabel = tk.Label(self,text = "Enter your Server Details:")
        self.titleLabel.grid(row = 0, columnspan = 2,padx = 30,pady = 10)
        
        self.serverLabel = tk.Label(self,text = "ServerAddress:")
        self.portLabel = tk.Label(self,text = "Port:")
        self.serverLabel.grid(row = 1,padx = 30,pady = 10)
        self.portLabel.grid(row = 2,padx = 30,pady = 10)
        
        self.serverEntry = tk.Entry(self)
        self.portEntry = tk.Entry(self)
        self.serverEntry.grid(row = 1,column = 1,padx = 10,pady = 10)
        self.portEntry.grid(row = 2,column = 1,padx = 10,pady = 10)
        
        submitButton = tk.Button(self, text = "Connect",command = lambda:self.Connect())
        submitButton.grid(row = 3, column = 0,columnspan = 2,pady = 10)
        
    def Connect(self):
        server = self.serverEntry.get()
        port = self.portEntry.get()
        self.controllerWindow.DisplayPage("Login")
            
        
class Login(tk.Frame):
    def __init__(self,window,controllerWindow):
        tk.Frame.__init__(self, window)
        self.window = window
        self.controllerWindow = controllerWindow
        
        self.titleLabel = tk.Label(self,text = "Please enter your Login Details:")
        self.titleLabel.grid(row = 0, columnspan = 2,padx = 30,pady = 10)
        
        self.usernameLabel = tk.Label(self,text = "Username:")
        self.passwordLabel = tk.Label(self,text = "Password:")
        self.usernameLabel.grid(row = 1,padx = 40,pady = 10)
        self.passwordLabel.grid(row = 2,padx = 40,pady = 10)
        
        self.usernameEntry = tk.Entry(self)
        self.passwordEntry = tk.Entry(self)
        self.usernameEntry.grid(row = 1,column = 1,padx = 10,pady = 10)
        self.passwordEntry.grid(row = 2,column = 1,padx = 10,pady = 10)
        
        submitButton = tk.Button(self, text = "Login",command = lambda:self.CaptureLoginDetails())
        submitButton.grid(row = 3, column = 0,columnspan = 2,pady = 10)
        
    def CaptureLoginDetails(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        self.controllerWindow.DisplayPage("UploadDownload")
        
        
class UploadDownload(tk.Frame):
    def __init__(self, window,controllerWindow):
        tk.Frame.__init__(self, window)
        self.window = window
        self.controllerWindow = controllerWindow
        uploadButton = tk.Button(self, text = "Upload A File",
                                 command = lambda:self.controllerWindow.DisplayPage("Upload"))
        uploadButton.grid(row = 1, column = 1, padx = 30,pady = 40)
        
        downloadButton = tk.Button(self, text = "Download A File",
                                   command = lambda:self.controllerWindow.DisplayPage("Download"))
        downloadButton.grid(row = 1, column = 2, padx = 20, pady = 40)
        
     
class Download(tk.Frame):
    def __init__(self, window,controllerWindow):
        tk.Frame.__init__(self, window)
        self.window = window
        self.controllerWindow = controllerWindow

        self.downloadLabel = tk.Label(self,text = "Select a file to download")
        self.downloadLabel.grid(row = 0,padx = 30,pady = 10, columnspan = 2)
        
        self.downloadList = tk.Listbox(self, height = 10)
        self.downloadList.grid(sticky = tk.E,row = 1, column = 0,columnspan = 1, padx = 20, pady = 20)
        
        filenames = self.GetFileList()
        for filename in filenames:
            self.downloadList.insert(tk.END, filename)
        
        if len(filenames)>10:
            scrollbar = tk.Scrollbar(self)
            scrollbar.grid(sticky=tk.E + tk.N + tk.S, row = 1, columnspan = 1, column = 0, pady = 20)
            self.downloadList.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.downloadList.yview)
        
        downloadButton = tk.Button(self, text = "Download", command = lambda:self.Download())
        downloadButton.grid(row = 1, column = 2, padx = 20, pady = 40)
        
    def GetFileList(self):
        fileList = {0,1,3,2,4,5,6,7,8,9,10,11}
        return sorted(fileList)
    
    def Download(self):
        filename = self.downloadList.get(self.downloadList.curselection()[0])
        print filename

class Upload(tk.Frame):
    def __init__(self, window,controllerWindow):
        tk.Frame.__init__(self, window)
        self.window = window
        self.controllerWindow = controllerWindow

        self.upLabel = tk.Label(self,text = "Enter a filepath to upload")
        self.upLabel.grid(row = 0,padx = 30,pady = 10)
        
        self.uploadEntry = tk.Entry(self)
        self.uploadEntry.grid(row = 1,padx = 10,pady = 10)
        
        uploadButton = tk.Button(self, text = "Upload", command = lambda:self.Upload())
        uploadButton.grid(row = 2, padx = 20, pady = 40)
        
    def Upload(self):
        uploadPath = self.uploadEntry.get()
        print uploadPath
    
        
FTPGUI = FTPGUI()
FTPGUI.mainloop()
