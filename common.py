import tkinter
from tkinter import messagebox
from tkinter import filedialog

replyed = 0

def intiate():
    global root
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
#

def errormsg(title,message):
    root.deiconify()
    messagebox.showerror(title=title, message=message)
    root.withdraw()
#

def infomsg(title,message):
    root.deiconify()
    messagebox.showinfo(title=title, message=message)
    root.withdraw()
#

def pointtodir(title): #in case of direct intaraction with folders
    root.deiconify()
    res = filedialog.askdirectory(title=title)
    root.withdraw()
    return res
#

class infopopup: #to show information whithout requiring users action
    def __init__(self,parent):
        self.top = tkinter.Toplevel(parent)
        self.top.attributes("-topmost", 1)
        self.lab = tkinter.Label(self.top,text = '')
        self.lab.pack()
    #

    def show(self,newtext):
        self.lab['text'] = newtext
        self.lab.update()
    #        

    def close(self):
        self.top.destroy()
    #
#
