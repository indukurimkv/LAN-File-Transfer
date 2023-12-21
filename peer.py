from client import sync
from server import runServer
import pickle
from threading import Thread

import time 

def runClient(syncDir, masterAddress, reloadTime = 30):
    while True:
        sync(syncDir, masterAddress=masterAddress)
        time.sleep(reloadTime)

if __name__ == "__main__":
    with open("./global.cfg", "rb") as file:
        config = pickle.load(file)
    
    clientThread = Thread(target = runClient, args=(
        config["SyncDir"],
        config["SourceAddress"]
    ))
    serverThread = Thread(target=runServer, args=(config["SyncDir"], ))

    clientThread.start()
    serverThread.start()

    clientThread.join()
    serverThread.join()
    