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

def peer(config):
    sourceAddr = config["SourceAddress"]
    maxConnections = config["maxConnections"]
    syncDir = config["SyncDir"]

    lockClient = [False]
    
    clientThread = Thread(target = runClient, args=(
        syncDir,
        sourceAddr,
        lockClient,
        config["ClientRetryTime"]
    ))
    serverThread = Thread(target=runServer, 
        args=(syncDir, lockClient), 
        kwargs={"maxConnections":maxConnections}
    )

    clientThread.start()
    serverThread.start()

    clientThread.join()
    serverThread.join()
    