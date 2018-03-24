import Tkinter as tk
import tkMessageBox
import Project_Client as cl

class FTPGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Somewhat FTP")
        self.hasClient= False
        self.protocol("WM_DELETE_WINDOW", self.CloseApp)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        self.frames = {}
        for Frameclass in (ChooseServer, Login, UploadDownload, Download, Upload):
            pageName = Frameclass.__name__
            frame = Frameclass(container, self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="NSEW")
    
        self.DisplayPage("ChooseServer")
        
                
    def DisplayPage(self,pageName):
        for frame in self.frames.values():
            frame.grid_remove()
            
        frame = self.frames[pageName]
        frame.grid()
        
    def CloseApp(self):
        if self.hasClient == False:
            self.destroy()
        else:
            self.client.Quit()
            self.destroy()

       
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
        try:
            self.controllerWindow.client = cl.ClientHandler(server, port)
            self.controllerWindow.hasClient = True
            self.controllerWindow.DisplayPage("Login")
        except:
            tkMessageBox.showinfo("Connection Error", "The server you tried to connect to did not respond or denied you request")
            self.controllerWindow.DisplayPage("ChooseServer")
            
       
            
        
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
        try:
            self.controllerWindow.client.Login(username, password)
            self.controllerWindow.DisplayPage("UploadDownload")
        except cl.LoginError:
            tkMessageBox.showinfo("Login Error", "The Login Details you entered were incorrect")
            self.controllerWindow.DisplayPage("Login")
       
        
        
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

        self.downloadLabel = tk.Label(self,text = "Select a file to download and the path to download to")
        self.downloadLabel.grid(row = 0,padx = 30,pady = 10, columnspan = 4)
        
        self.downloadList = tk.Listbox(self, height = 10)
        self.downloadList.grid(sticky = tk.E,row = 1, column = 0,columnspan = 1, padx = 10, pady = 10)
        
        filenames = self.GetFileList()
        for filename in filenames:
            self.downloadList.insert(tk.END, filename)
        
        if len(filenames)>10:
            scrollbar = tk.Scrollbar(self)
            scrollbar.grid(sticky=tk.E + tk.N + tk.S, row = 1, columnspan = 1, column = 0, pady = 10)
            self.downloadList.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.downloadList.yview)
        
        self.downloadPathLabel = tk.Label(self, text = "Path to Download to:")
        self.downloadPathLabel.grid(row = 1,column = 2,padx = 5,pady = 5)
        
        self.downloadPathEntry = tk.Entry(self)
        self.downloadPathEntry.grid(row = 1,column = 3,padx = 10,pady =5)
        
        downloadButton = tk.Button(self, text = "Download", command = lambda:self.Download())
        downloadButton.grid(row = 3, column = 0,columnspan = 4 ,padx = 5, pady = 5)
        
        backButton = tk.Button(self, text = "Back", command = lambda:self.controllerWindow.DisplayPage("UploadDownload"))
        backButton.grid(row = 4, column = 0,columnspan = 4, pady = 10)
        
    def GetFileList(self):
        try:
            fileList = self.controllerWindow.client.List(None)
            return sorted(fileList)
        except cl.DoesntExist:
            tkMessageBox.showinfo("Directory Error", "The Directory you tried to list does not exist on the server.")
            self.controllerWindow.DisplayPage("UploadDownload")
        except cl.LoginError:
            tkMessageBox.showinfo("Login Error", "You are not logged in.")
            self.controllerWindow.DisplayPage("Login")
            
      
    
    def Download(self):
        try:
            filename = self.downloadList.get(self.downloadList.curselection()[0])
            downloadPath = self.downloadPathEntry.get()
            try:
                self.controllerWindow.client.RETR(downloadPath,filename)
                tkMessageBox.showinfo("File Transfer in Progress", "The file you requested is being downloaded now. Please wait for it to finish before you continue.")
            except cl.BadConnection:
                tkMessageBox.showinfo("Connection Error", "There was an error with the data connection transfer. Please try again later")
                self.controllerWindow.DisplayPage("Download")
            except cl.DoesntExist as fde:
                tkMessageBox.showinfo("File Error", "The file: " + fde.fileName + " does not exist at the server")
                self.controllerWindow.DisplayPage("Download")
        except IndexError:
            tkMessageBox.showinfo("Selection Error", "Please Select a File before clicking download.")
        
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
        uploadButton.grid(row = 2, padx = 20, pady = 10)
        
        backButton = tk.Button(self, text = "Back", command = lambda:self.controllerWindow.DisplayPage("UploadDownload"))
        backButton.grid(row = 3, padx = 20, pady = 10)
        
    def Upload(self):
        uploadPath = self.uploadEntry.get()
        try:
            self.controllerWindow.client.STOR(uploadPath)
            self.controllerWindow.DisplayPage("UploadDownload")
        except cl.DoesntExist:
            tkMessageBox.showinfo("File Error", "The file you tried to send did not have the correct path or doesn't exist")
            self.controllerWindow.DisplayPage("Upload")
        except cl.AccessDenied:
            tkMessageBox.showinfo("Access Denied", "The server denied access to the transfer")
            self.controllerWindow.DisplayPage("Upload")
        except cl.LoginError:
            tkMessageBox.showinfo("Login Error", "You are not logged in.")
            self.controllerWindow.DisplayPage("Login")
        
FTPGUI = FTPGUI()
FTPGUI.mainloop()
