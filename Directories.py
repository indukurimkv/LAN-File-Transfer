from os import listdir, walk
from os.path import isfile, isdir, join

def getStructure(path):
    out = {},[]
    for item in listdir(path):
        if isdir(join(path, item)):
            out[0][item] = getStructure(join(path, item))
            continue
        out[1].append(item)
    return out
def diff(server, client):
    out = {}, []
    if server == out: return out
    
    # first check file discrepencies
    serverFiles = server[1]
    clientFiles = client[1]
    for file in serverFiles:
        if file not in clientFiles:
            out[1].append(file)
            
    serverDirs = server[0]
    clientDirs = client[0]
    
    for dir in serverDirs:
        # If a directory in server doesn't exist in client create it and diff
        if dir not in clientDirs:
            out[0][dir] = [dict(), list()]
            changes = diff(serverDirs[dir], out[0][dir])
        # If a directory in server exists in client, diff subdirectories/files
        else:
            changes = diff(serverDirs[dir], clientDirs[dir])
        # If diff is non-empty add it to the final output
        if changes != (dict(), list()):
            out[0][dir] = changes
    return out

        
            
if __name__ == "__main__":    
    masterDir = "./test/master"
    clientDir = "./test/client"

    print(diff(getStructure(masterDir), getStructure(clientDir)))



