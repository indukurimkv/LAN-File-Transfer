import pickle

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import re

class Config(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("350x150")
        self.resizable(True, False)
        self.title("LAN File Mirroring")
        self.header = Label(self, text="LAN File Mirroring").grid(row=0, column=0, columnspan=2)

        self.lanAddrLabel = Label(self, text="Host IP Address")
        self.sourceAddrLabel = Label(self, text="Source IP Address")
        self.isSourceLabel = Label(self, text="Host is Source")
        
        self.lanAddrIn = Entry(self)
        self.lanAddrIn.bind('<Return>', self.updateSourceAddr)
        self.lanAddrIn.bind('<Tab>', self.updateSourceAddr)
        self.sourceAddrInVar = StringVar()
        self.sourceAddrIn = Entry(self, textvariable=self.sourceAddrInVar)
        self.isSourceVar = BooleanVar()
        self.isSourceVar.set(False)
        self.isSourceCheck = ttk.Checkbutton(self, command=self.updateSourceAddr, variable=self.isSourceVar)


        self.askFolderLabel = Label(self, text="Folder to Sync")
        self.askFolderButton = Button(self, text="Select Folder", command=self.setFolder)
        self.syncDir = ''

        self.saveButton = Button(self, text="Save", command=self.save)

        self.lanAddrLabel.grid(row = 1, column = 0, sticky=W)
        self.isSourceLabel.grid(row=2, column=0, sticky=W)
        self.sourceAddrLabel.grid(row = 3, column = 0, sticky=W)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.lanAddrIn.grid(row = 1, column = 1, sticky=EW, padx=2.5)
        self.isSourceCheck.grid(row=2, column=1, sticky=W)
        self.sourceAddrIn.grid(row = 3, column = 1, sticky=EW, padx=2.5)

        self.askFolderLabel.grid(row=4, column=0, sticky=W)
        self.askFolderButton.grid(row=4, column=1, sticky=EW)
        
        self.saveButton.grid(row = 5, column=0, columnspan=2, sticky=EW)



        mainloop()
    
    def setFolder(self):
        self.syncDir = filedialog.askdirectory()
        print(self.syncDir)

    def validate(self):
        out = {}
        IPPattern = '^([0-9]{1,3}\\.){3}[0-9]{1,3}$'
        if re.match(IPPattern, lanAddr := self.lanAddrIn.get()) and \
            re.match(IPPattern, sourceAddr := self.sourceAddrIn.get()) and \
                self.syncDir:
            
            out["LANAddress"] = lanAddr
            out["SourceAddress"] = sourceAddr
            out["SyncDir"] = self.syncDir
            
            return out
    def save(self):
        if (config := self.validate()) == None:
            popUp = Toplevel(self)
            popUp.geometry("175x50")
            popUp.resizable(False, False)
            popUp.title("Error")
            Label(popUp, text="All fields must be complete\nand properly formatted!").pack()
            return
        
        with open('./global.cfg', "wb") as file:
            pickle.dump(config, file)
            print(f"Saved: \n{config}")
        self.quit()
    
    def updateSourceAddr(self, *args):
        if self.isSourceVar.get():
            self.sourceAddrInVar.set(
                self.lanAddrIn.get()
            )

        

if __name__ == "__main__":
    Config()
    globalConfig = {
        "LANAddress": "192.168.50.95",
        "SourceAddress": "192.168.50.183",
        "SyncDir": "./test/master"
    }

