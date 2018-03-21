from Tkinter import *

window = Tk()
window.resizable(0, 0)
frame = Frame(window)
class LoginScreen:
    def __init__(self,window):
        self.window = window
        self.window.geometry("300x150")
        self.window.title("Enter your credentials")
        self.usernameLabel = Label(self.window,text = "Username:")
        self.passwordLabel = Label(self.window,text = "Password:")
        self.usernameLabel.grid(row = 1,padx = 30,pady = 10)
        self.passwordLabel.grid(row = 2,padx = 30,pady = 10)
        
        self.usernameEntry = Entry(self.window)
        self.passwordEntry = Entry(self.window)
        self.usernameEntry.grid(row = 1,column = 1,padx = 10,pady = 10)
        self.passwordEntry.grid(row = 2,column = 1,padx = 10,pady = 10)
        
        submitButton = Button(self.window, text = "Login")
        submitButton.grid(row = 3, column = 1,columnspan = 2)
        
class FileExploreScreen:
    def __init__(self, window):
        self.window = window
        self.window.geometry("300x150")
        self.window.title("Download or Upload Files")     
        
        uploadButton = Button(self.window, text = "Upload A File")
        uploadButton.grid(row = 1, column = 1, padx = 20,pady = 20)
        
        downloadButton = Button(self.window, text = "Download A File")
        downloadButton.grid(row = 1, column = 2, padx = 20,pady = 20)
        
        
Screen = LoginScreen(root)
window.mainloop()
