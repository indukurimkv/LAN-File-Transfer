import socket
import time
from Directories import getStructure
import tqdm
import pickle

# General function to get connection info from peers
def getConnectionInfo(serverAddress = "127.0.0.1", serverPort = 50000):    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((serverAddress, serverPort))
        # recieve info
        data = s.recv(128)
    return data.decode()

# Gets address of peer to send/recieve file data
getConnectionAddress = lambda *args: str(getConnectionInfo(*args))
# Gets the port from peer on which to send/recieve file data
getConnectionPort = lambda *args: int(getConnectionInfo(*args))

def syncFiles(structure, root, connection: socket.socket, chunkSize = None):
    dirs, files = structure
    diffLength = "{:<128}".format(len(diff := pickle.dumps(structure)))
    
    connection.sendall(diffLength.encode())
    connection.sendall(diff)
    
    if chunkSize == None:
        try:
            chunkSize = int(connection.recv(128))
        except:
            chunkSize = 10
    
    for file in files:
        filePath = f"{root}/{file}"
        remainingBytes = int(connection.recv(128).decode())
        with open(filePath, "wb") as file:
            pbar = tqdm.tqdm(total=remainingBytes)
            while remainingBytes > 0:
                input = connection.recv(min(chunkSize, remainingBytes))
                file.write(input)
                remainingBytes -= chunkSize
                pbar.update(chunkSize)
            pbar.close()
            print("wrote ", file)
            
    for dir in dirs:
        syncFiles(dirs[dir], f"{root}/{dir}", connection, chunkSize)

with socket.create_connection(('', getConnectionPort())) as con:
    syncFiles(
        ({}, ['ubuntu-22.04.2-desktop-amd64.iso']),
        './test/client',
        con
    )
    