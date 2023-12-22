from backend.client import sync
from backend.server import runServer
from backend.Interfaces import getInterfaces
import pickle
from threading import Thread

import time 

def runClient(syncDir, masterAddress, lockClient, reloadTime = 30):
    while True:
        if lockClient[0]:
            continue

        sync(syncDir, masterAddress=masterAddress)
        time.sleep(reloadTime)

if __name__ == "__main__":
    with open("./global.cfg", "rb") as file:
        config = pickle.load(file)
    sourceAddr = config["SourceAddress"]

    lockClient = [True]
    
    clientThread = Thread(target = runClient, args=(
        config["SyncDir"],
        sourceAddr,
        lockClient
    ))
    serverThread = Thread(target=runServer, args=(config["SyncDir"], lockClient))

    clientThread.start()
    serverThread.start()

    clientThread.join()
    serverThread.join()
    