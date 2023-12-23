import threading
from backend.master import runMaster
from backend.server import runServer
import pickle

def source(config):
    maxConnections = config["maxConnections"]

    masterThread = threading.Thread(target=runMaster, 
        args=(config["SyncDir"], ),
        kwargs={"maxConnections": maxConnections}
        )
    
    serverThread = threading.Thread(target=runServer, 
        args=(config["SyncDir"], [False]),
        kwargs={"maxConnections": maxConnections}
        )
    masterThread.start()
    serverThread.start()

    masterThread.join()
    serverThread.join()

