import socket
import time
from Directories import getStructure
import tqdm
import pickle
import os
import random
from threading import Thread
import uuid
from utils import safeSend, safeRecv

# General function to get connection info from peers
def getConnectionPort(serverAddress = "127.0.0.1", serverPort = 50000):  
    print("getting port on peer")  
    with socket.create_connection((serverAddress, serverPort)) as sock:
        # recieve info
        data = sock.recv(128)
    try:
        return int(data.decode())
    except:
        print("Unable to convert recieved port to int.")

# Contact master server to get files to sync and peers to sync with
def getDiff(clientStrcut, masterAddress = '', masterPort = 45000):
    with socket.create_connection((masterAddress, masterPort)) as sock:
        clientBytes = pickle.dumps(clientStrcut)
        try:
            sock.sendall("{:<128}".format(len(clientBytes)).encode())
            sock.sendall(clientBytes)
            serverMessageLen = int(sock.recv(128).decode())
            serverMessage = pickle.loads(sock.recv(serverMessageLen))
            if serverMessage == "synced":
                return
            diff, addrs = serverMessage
            return diff, addr if (addr := random.choice(addrs)) != '0.0.0.0' else '127.0.0.1'
        except:
            print("Unable to contact server.")
        
        

def makeDirs(structure, root):
    dirs, _ = structure
    if len(dirs) == 0:
        try:
            os.makedirs(root)
        except FileExistsError:
            print(f"dir: {root} already exists. skipping.")
        return
    for dir in dirs:
        makeDirs(dirs[dir], f"{root}/{dir}")

def recursiveMirror(structure, root, connection: socket.socket):
    print("syncing")
    makeDirs(structure, root)

    # Send server diff info to recieve files
    # Only send on first recursion
    safeSend(structure, connection)
    # Get chunk size from server
    chunkSize = safeRecv(connection)
    
    def traverseDirs(structure, root):
        dirs, files = structure

        for file in files:
            filePath = f"{root}/{file}"

            # get bytes left to read on file returned by loader function on server
            remainingBytes = int(connection.recv(128, socket.MSG_WAITALL).decode())
            with open(filePath, "wb") as outFile:
                pbar = tqdm.tqdm(total=remainingBytes)
                while remainingBytes > 0:
                    # Get largest frame smaller than number of bytes left to read 
                    input = connection.recv(min(chunkSize, remainingBytes))
                    outFile.write(input)
                    remainingBytes -= chunkSize
                    
                    pbar.update(chunkSize)
                pbar.close()
            
            print(connection.recv(3, socket.MSG_WAITALL).decode(), "wrote ", file)
                
        for dir in dirs:
            traverseDirs(dirs[dir], f"{root}/{dir}")
    
    traverseDirs(structure, root)

def sync(root, chunkSize = None, masterAddress = '127.0.0.1'):
    print(f"Attempting sync on {masterAddress}")
    while (diffInfo := getDiff(getStructure(root), masterAddress=masterAddress)) != None:
        diff, addr = diffInfo
        print(f"peer address {addr}")
        with socket.create_connection((addr, port := getConnectionPort(addr))) as connection:
            print(f"peer info: {addr}:{port}")        
            recursiveMirror(diff, root, connection)
            
            safeSend("Clean Exit", connection)
            closeConfirm = safeRecv(connection)
            print(f"{closeConfirm} from {addr}:{port}")

        currentStructure = getStructure(root)
            

if __name__ == "__main__":
    with open("./global.cfg", 'rb') as file:
        globalConfig = pickle.load(file)

    for i in range(1):
        threads = [Thread(target=lambda x: sync(f"./test/client{uuid.uuid4().hex}", masterAddress=globalConfig["LANAddress"]), args=(i,)) for i in range(1)]
        [i.start() for i in threads]
        [i.join() for i in threads]