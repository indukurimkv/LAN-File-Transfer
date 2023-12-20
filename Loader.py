import os
from os.path import join

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
    for dir in dirs:
        yield from getBytes(dirs[dir], f"{root}/{dir}", chunkSize)
        
        
if __name__ == "__main__":    
    masterDir = "./test/master"
    clientDir = "./test/client"

    structure = diff(getStructure(masterDir), getStructure(clientDir))
    print(structure)

    [print(i) for i in getBytes(structure, "./test/master")]


