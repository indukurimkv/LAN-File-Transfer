import socket
from threading import Thread
import time
import pickle
from Loader import getBytes

def Print(*args):
    print("[Server]", *args)

class Listener(Thread):
    def __init__(self, port=0, directory = "./master") -> int:
        super().__init__()
        self.sock = socket.create_server(('', port))
        self.PORT = self.sock.getsockname()[1]
        self.DIR = directory
        
        self.connTracker = None

    def subscribeToConnectionUpdates(self, connections):
        self.connTracker = connections
    
    def sendData(self):
        with self.sock:
            self.sock.listen()
            conn, self.clientAddr = self.sock.accept()
            diffLength = int(conn.recv(128).decode())
            diff = pickle.loads(conn.recv(diffLength))
            Print("Syncing the following with {}".format(self.clientAddr))
            Print(diff)
            
            
            conn.sendall("{:<128}".format(4096).encode())
            for byteGroup in getBytes(diff, "./test/master"):
                conn.sendall(byteGroup)
            
            conn.sendall(conn.recv(16, socket.MSG_WAITALL))
            
                
    def run(self) -> None:
        try: 
            self.sendData()
            self.close()
        except Exception as e:
            Print(e) 
            self.close()    
      
    def close(self):
        Print("closed connection with {}".format(self.clientAddr))
        if self.connTracker != None:
            self.connTracker.remove(self.PORT)      


    def start(self) -> None:
        Print(self.connTracker)
        if self.connTracker != None:
            self.connTracker.append(self.PORT)
        super().start()

def runServer():
    connections = []
    Print('Running on 0.0.0.0')
    with socket.create_server(('', 50000)) as s:
        s.listen()
        while True:
            if(len(connections) >=30): continue
            conn, addr = s.accept()
            with conn:
                Print('connected with', addr)
                listener = Listener()
                listener.subscribeToConnectionUpdates(connections)
                listener.start()
                conn.sendall("{:<128}".format(listener.PORT).encode())

if __name__ == "__main__":    
    runServer()