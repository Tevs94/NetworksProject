from Tkinter import *

root = Tk()
root.geometry("300x200")
root.resizable(0, 0)

class LoginScreen:
    def __init__(self,root):
        self.window = root
        self.window.title("Enter your credentials")
        self.usernameLabel = Label(self.window,text = "Username")
        self.passwordLabel = Label(self.window,text = "Password")
        self.usernameLabel.grid(row = 1,sticky = SE,padx = 30,pady = 10)
        self.passwordLabel.grid(row = 2,sticky = SE,padx = 30,pady = 10)
        
        self.usernameEntry = Entry(self.window)
        self.passwordEntry = Entry(self.window)
        self.usernameEntry.grid(row = 1,column = 1,sticky = N)
        self.passwordEntry.grid(row = 2,column = 1,sticky = N)
        
        submitButton = Button(self.window, text = "Login")
        submitButton.grid(row = 3, column = 1,sticky = N)
        

Login = LoginScreen(root)
root.mainloop()
