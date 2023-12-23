import pickle

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
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

        self.geometry("350x175")
        self.resizable(True, False)
        self.title("LAN File Mirroring")
        self.iconbitmap('./icon.ico')
        self.header = Label(self, text="LAN File Mirroring").grid(row=0, column=0, columnspan=2)
        
        self.lanAddrVar = StringVar()
        self.lanAddrVar.set(interfaceNames[0])
        self.lanAddrSelection = OptionMenu(self, self.lanAddrVar, *interfaceNames, command=self.updateSourceAddr)
        

        self.clientRetryTimeEntry = Entry(self)
        self.clientRetryTimeEntry.insert(END, "30")

        self.maxConnectionsEntry = Entry(self)
        self.maxConnectionsEntry.insert(END, "3")
        

        self.sourceAddrInVar = StringVar()
        self.sourceAddrIn = Entry(self, textvariable=self.sourceAddrInVar)
        self.isSourceVar = BooleanVar()
        self.isSourceVar.set(False)
        self.isSourceCheck = ttk.Checkbutton(self, command=self.updateSourceAddr, variable=self.isSourceVar)


        self.askFolderButton = Button(self, text="Select Folder", command=self.setFolder)
        self.syncDir = ''

        self.saveButton = Button(self, text="Save", command=self.save)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.makeWidgets((
            ("Host NIC", self.lanAddrSelection),
            ("Host is Source", self.isSourceCheck),
            ("Re-Sync Time", self.clientRetryTimeEntry),
            ("Max Connections", self.maxConnectionsEntry),
            ("Source Address", self.sourceAddrIn),
            ("Mirror Folder", self.askFolderButton)
        ))
        
        self.saveButton.grid(row = 6, column=0, columnspan=2, sticky=EW, padx=2.5, pady=2.5)



        mainloop()
    def makeWidgets(self, template):
        for i, (labelText, widget) in enumerate(template):
            label = Label(self, text=labelText)
            label.grid(row=i, column=0, sticky=W, padx=2.5)
            widget.grid(row=i, column=1, sticky=EW,padx=2.5)
            
    def setFolder(self):
        self.syncDir = filedialog.askdirectory()
        print(self.syncDir)

    def validate(self):
        out = {}
        IPPattern = "^([0-9]{1,3}\\.){3}[0-9]{1,3}$"
        
        hostInt = self.lanAddrVar.get()
        try:
            retryTime = int(self.clientRetryTimeEntry.get())
            maxConnections = int(self.maxConnectionsEntry.get())
        except:
            return
        if re.match(IPPattern, sourceAddr := self.sourceAddrIn.get()) and \
                self.syncDir:
            
            out["LANAddress"] = hostInt, self.interfaces[hostInt][0]
            out["SourceAddress"] = sourceAddr
            out["SyncDir"] = self.syncDir
            out["ClientRetryTime"] = retryTime
            out["maxConnections"] = maxConnections
            out["isSource"] = self.isSourceVar.get()
            
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

