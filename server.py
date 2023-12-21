import socket
from threading import Thread
import time
import pickle
from Loader import getBytes

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
            print("Syncing the following with {}".format(self.clientAddr))
            print(diff)
            
            
            conn.sendall("{:<128}".format(4096).encode())
            for byteGroup in getBytes(diff, "./test/master"):
                conn.sendall(byteGroup)
            
                
    def run(self) -> None:
        try: 
            self.sendData()
            self.close()
        except Exception as e:
            print(e) 
            self.close()    
      
    def close(self):
        print("closed connection with {}".format(self.clientAddr))
        if self.connTracker != None:
            self.connTracker.remove(self.PORT)      

    def start(self) -> None:
        print(self.connTracker)
        if self.connTracker != None:
            self.connTracker.append(self.PORT)
        super().start()

def runServer():
    connections = []

    with socket.create_server(('', 50000)) as s:
        s.listen()
        while True:
            if(len(connections) >=30): continue
            conn, addr = s.accept()
            with conn:
                print('connected with', addr)
                listener = Listener()
                listener.subscribeToConnectionUpdates(connections)
                listener.start()
                conn.sendall("{:<128}".format(listener.PORT).encode())

if __name__ == "__main__":    
    runServer()