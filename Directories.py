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
    # first check file discrepencies
    serverFiles = server[1]
    clientFiles = client[1]
    for file in serverFiles:
        if file not in clientFiles:
            out[1].append(file)
    
    
masterDir = "./test/master"
clientDir = "./test/client"

print(getStructure(masterDir))



