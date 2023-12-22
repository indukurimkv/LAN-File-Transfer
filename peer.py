from backend.client import sync
from backend.server import runServer
from backend.Interfaces import getInterfaces
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
    sourceAddr = config["SourceAddress"]
    
    clientThread = Thread(target = runClient, args=(
        config["SyncDir"],
        sourceAddr
    ))
    serverThread = Thread(target=runServer, args=(config["SyncDir"], ))

    clientThread.start()
    serverThread.start()

    clientThread.join()
    serverThread.join()
    