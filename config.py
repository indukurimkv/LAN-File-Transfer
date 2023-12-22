import pickle

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import re

from backend.Interfaces import getInterfaces
    
class Config(Tk):
    def __init__(self):
        super().__init__()
        self.interfaces = getInterfaces()
        interfaceNames = list(self.interfaces.keys())
        
        if(len(self.interfaces) == 0):
            print("No NICs Found!")
            return

        self.geometry("350x150")
        self.resizable(True, False)
        self.title("LAN File Mirroring")
        self.header = Label(self, text="LAN File Mirroring").grid(row=0, column=0, columnspan=2)

        self.lanAddrLabel = Label(self, text="Host NIC")
        self.sourceAddrLabel = Label(self, text="Source IP")
        self.isSourceLabel = Label(self, text="Host is Source")
        
        self.lanAddrVar = StringVar()
        self.lanAddrVar.set(interfaceNames[0])
        self.lanAddrSelection = OptionMenu(self, self.lanAddrVar, *interfaceNames, command=self.updateSourceAddr)
        
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

        self.lanAddrSelection.grid(row = 1, column = 1, sticky=EW, padx=2.5)
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
        IPPattern = "^([0-9]{1,3}\\.){3}[0-9]{1,3}$"
        
        hostInt = self.lanAddrVar.get()
        if re.match(IPPattern, sourceAddr := self.sourceAddrIn.get()) and \
                self.syncDir:
            
            out["LANAddress"] = hostInt, self.interfaces[hostInt][0]
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
            name = self.lanAddrVar.get()
            self.sourceAddrInVar.set(self.interfaces[name][1])

        

if __name__ == "__main__":
    Config()

