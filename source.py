import threading
from master import runMaster
from server import runServer
import pickle

if __name__ == "__main__":
    with open("./global.cfg", 'rb') as file:
        config = pickle.load(file)
    
    masterThread = threading.Thread(target=runMaster, args=(config["SyncDir"], ))
    serverThread = threading.Thread(target=runServer, args=(config["SyncDir"], ))
    masterThread.start()
    serverThread.start()

    masterThread.join()
    serverThread.join()

