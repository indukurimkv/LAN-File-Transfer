import socket
import traceback
import tqdm
import pickle
import os
import random
from threading import Thread
import uuid

from backend.Directories import getStructure
from backend.utils import safeSend, safeRecv, recieveAll
from backend.Interfaces import confToIp

def Print(*args):
    print("[Client]", *args)

# General function to get connection info from peers
def getConnectionPort(serverAddress = "127.0.0.1", serverPort = 50000):  
    Print("getting port on peer")  
    with socket.create_connection((serverAddress, serverPort), timeout=5) as sock:
        # recieve info
        data = recieveAll(128, sock)
    try:
        return int(data.decode())
    except:
        Print("Unable to convert recieved port to int.")

# Contact master server to get files to sync and peers to sync with
def getDiff(clientStrcut, masterAddress = '', masterPort = 45000):
    try:
        with socket.create_connection((masterAddress, masterPort), timeout=5) as sock:

            safeSend(clientStrcut, sock)
            serverMessage = safeRecv(sock)

            if serverMessage == "synced":
                return
            diff, addrs = serverMessage
            return diff, addr if (addr := random.choice(addrs)) != '0.0.0.0' else '127.0.0.1'
    except Exception as e:
        Print("Unable to contact server.")
        Print(e)
        
        

def makeDirs(structure, root):
    dirs, _ = structure
    if len(dirs) == 0:
        try:
            os.makedirs(root)
        except FileExistsError:
            Print(f"dir: {root} already exists. skipping.")
        return
    for dir in dirs:
        makeDirs(dirs[dir], f"{root}/{dir}")

def recursiveMirror(structure, root, connection: socket.socket):
    Print("syncing")
    makeDirs(structure, root)

    # Send server diff info to recieve files
    # Only send on first recursion
    safeSend(structure, connection)
    
    def traverseDirs(structure, root):
        dirs, files = structure

        for file in files:
            filePath = f"{root}/{file}"

            # get bytes left to read on file returned by loader function on server
            fileSize = int(recieveAll(128, connection).decode())
            Print(f"Writing {file}")
            with open(filePath, "wb") as outFile:
                pbar = tqdm.tqdm(total=fileSize)

                # Recieve all bytes of file
                # Callback writes file to local dir and updates pbar
                recieveAll(
                    fileSize,
                    connection,
                    onRecieve= lambda x: pbar.update(
                        outFile.write(x)
                    )
                )
                timeToWrite = pbar.format_dict["elapsed"]
                pbar.close()
            if (writtenSize := os.stat(filePath).st_size) == fileSize:
                Print(f"Wrote {fileSize} bytes in {timeToWrite} seconds")
            else:
                Print(f"Only wrote {writtenSize}/{fileSize} bytes to {file}.")
                Print(f"Aborting sync for {file}")
                try: os.remove(filePath)
                except: Print(f"""Failed to remove incomplete file: {file}. Manually delete it to resync.""")
                
        for dir in dirs:
            traverseDirs(dirs[dir], f"{root}/{dir}")
    try:
        traverseDirs(structure, root)
        return 0
    except Exception as e:
        Print("Error cloning directory")
        traceback.print_exc()
        return -1

def sync(root, chunkSize = None, masterAddress = '127.0.0.1'):
    Print(f"Attempting sync on {masterAddress}")
    while (diffInfo := getDiff(getStructure(root), masterAddress=masterAddress)) != None:
        
        diff, addr = diffInfo
        Print(f"peer address {addr}")
        
        # Talk to peer to negotiate private port for P2P sync
        try: port = getConnectionPort(addr) 
        except: Print("Unable to negotiate port on peer"); return

        with socket.create_connection((addr, port)) as connection:
            Print(f"peer info: {addr}:{port}")  

            # Attempt to clone directory from master and exit on error      
            if recursiveMirror(diff, root, connection) == -1:
                break
            
            safeSend("Clean Exit", connection)
            closeConfirm = safeRecv(connection)
            Print(f"{closeConfirm} from {addr}:{port}")

        currentStructure = getStructure(root)
            

if __name__ == "__main__":

    for i in range(1):
        threads = [Thread(target=lambda x: sync(f"./test/client", masterAddress=confToIp("LANAddress", './global.cfg')), args=(i,)) for i in range(1)]
        [i.start() for i in threads]
        [i.join() for i in threads]