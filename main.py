import threading
from master import runMaster
from server import runServer


if __name__ == "__main__":
    masterThread = threading.Thread(target=runMaster)
    serverThread = threading.Thread(target=runServer)
    masterThread.start()
    serverThread.start()

    masterThread.join()
    serverThread.join()

