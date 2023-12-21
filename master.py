from Directories import getStructure, diff
import socket
import pickle

def Print(*args):
    print("[Master]", *args)

def runMaster():
    root = './test/master'
    clients = {}
    with open("./global.cfg", "rb") as file:
        globalConfig= pickle.load(file)

    NICAddress = globalConfig["LANAddress"]

    with socket.create_server(('', 45000)) as sock:
        Print(f"Running on {sock.getsockname()[0]}")
        clients[NICAddress] = True
        lastStructure = None
        
        sock.listen()
        while True:
            conn, (addr, port) = sock.accept()
            Print(f"connected to {addr}")
            if len(clients) > 30 and addr not in clients:
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
                continue
            
            with conn:
                clientStructureLen = int(conn.recv(128).decode())
                clientStructure = pickle.loads(conn.recv(clientStructureLen))
                clients[addr] =  False
                
                
                masterStructure = getStructure(root)
                clientDiff = diff(masterStructure, clientStructure)
                if lastStructure != masterStructure:
                    clients = {NICAddress: True}
                clients[NICAddress] = True
                if clientDiff == ({}, []):
                    clients[addr] = True
                    Print(f"{addr} is synced")
                    message = pickle.dumps("synced")
                else:
                    message = pickle.dumps((clientDiff,
                                            syncedClients := [i for i in clients if clients[i]]))
                    Print(f"Sending diff to {addr}:\n{message}")
                    Print("Viable Peers:", syncedClients)
                conn.sendall("{:<128}".format(len(message)).encode())
                conn.sendall(message)
                
                lastStructure = masterStructure
                
        
        
if __name__ == '__main__':
    runMaster()       
        