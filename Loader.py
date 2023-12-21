import os
from os.path import join
import time
from Directories import diff, getStructure

def getBytes(structure, root, chunkSize = 4096):
    dirs, files = structure
    for file in files:
        filePath = root + "/" + file
        with open(join(root, file), 'rb') as file:
            remainingBytes = os.stat(filePath).st_size
            yield '{:<128}'.format(remainingBytes).encode()
            print(f"sending {remainingBytes} bytes")
            while remainingBytes > 0:
                yield file.read(chunkSize)
                remainingBytes -= chunkSize
        yield b'EOF'
    for dir in dirs:
        yield from getBytes(dirs[dir], f"{root}/{dir}", chunkSize)
        
        
if __name__ == "__main__":    
    masterDir = "./test/master"
    clientDir = "./test/client"

    structure = diff(master:=getStructure(masterDir), client:=getStructure(clientDir))
    print(master)
    print(client)
    print(structure)




