import os
from os.path import join
import time

from backend.Directories import diff, getStructure

def Print(*args):
    print("[Loader]", *args)

def getBytes(structure, root, chunkSize = 4096):
    dirs, files = structure
    for file in files:
        filePath = root + "/" + file

        try:
            with open(join(root, file), 'rb') as file:
                remainingBytes = os.stat(filePath).st_size
                yield '{:<128}'.format(remainingBytes).encode()
                while remainingBytes > 0:
                    yield file.read(chunkSize)
                    remainingBytes -= chunkSize
            yield b'EOF'
        except Exception as e:
            Print(f"Could not open directory {join(root,file)}. Stopping Sync")
            Print(e)
            yield -1
    for dir in dirs:
        yield from getBytes(dirs[dir], f"{root}/{dir}", chunkSize)
        
        
if __name__ == "__main__":    
    masterDir = "./test/master"
    clientDir = "./test/client"

    structure = diff(master:=getStructure(masterDir), client:=getStructure(clientDir))
    Print(master)
    Print(client)
    Print(structure)




