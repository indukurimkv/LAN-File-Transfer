import socket
from threading import Thread
import time
import pickle

from backend.Loader import getBytes
from backend.utils import safeSend, safeRecv

def Print(*args):
    print("[Server]", *args)

class Listener(Thread):
    def __init__(self, syncDirectory, port=0) -> int:
        super().__init__()
        self.sock = socket.create_server(('', port))
        self.PORT = self.sock.getsockname()[1]
        self.DIR = syncDirectory
        
        self.connTracker = None

    def subscribeToConnectionUpdates(self, connections, clientLock = None):
        self.clientLock = clientLock
        self.connTracker = connections
    
    def sendData(self):
        with self.sock:
            self.sock.listen()
            conn, self.clientAddr = self.sock.accept()
            
            diff = safeRecv(conn)
            Print("Syncing with {}".format(self.clientAddr))
            
            
            for byteGroup in getBytes(diff, self.DIR):
                # Make sure file is found before sending data
                if byteGroup == -1:
                    raise FileNotFoundError("File or directory could not be found.")
                
                conn.sendall(byteGroup)
            
            safeSend(safeRecv(conn), conn)
            
                
    def run(self) -> None:
        try: 
            self.sendData()
            self.close()
        except Exception as e:
            Print(e) 
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.close()    
      
    def close(self):
        Print("closed connection with {}".format(self.clientAddr))
        if self.connTracker != None:
            self.connTracker.remove(self.PORT)   
        
        if self.clientLock != None:
            self.clientLock[0] = len(self.connTracker) > 0
            Print(f"Host Locked: {self.clientLock[0]}")



    def start(self) -> None:
        Print(self.connTracker)
        if self.connTracker != None:
            self.connTracker.append(self.PORT)
        if self.clientLock != None:
            self.clientLock[0] = True
            Print(f"Host Locked: True")

        super().start()

def runServer(syncDir, lockClient, maxConnections=3):
    connections = []
    Print('Running on 0.0.0.0')
    with socket.create_server(('', 50000)) as s:
        s.listen()
        while True:
            if((numConn := len(connections)) >=maxConnections): continue
            
            conn, addr = s.accept()
            with conn:
                Print('connected with', addr)
                listener = Listener(syncDir)
                listener.subscribeToConnectionUpdates(connections, lockClient)
                listener.start()
                safeSend(listener.PORT, conn)

if __name__ == "__main__":    
    runServer("./test/master")