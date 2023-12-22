import socket
import pickle
import traceback

from backend.utils import safeSend, safeRecv
from backend.Directories import getStructure, diff
from backend.Interfaces import confToIp


def Print(*args):
    print("[Master]", *args)

def runMaster(root):
    clients = {}

    NICAddress = confToIp("LANAddress", "./global.cfg")

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
            
            try: 
                with conn:
                    clientStructure = safeRecv(conn)
                    clients[addr] =  False
                    
                    
                    masterStructure = getStructure(root)
                    clientDiff = diff(masterStructure, clientStructure)
                    if lastStructure != masterStructure:
                        clients = {NICAddress: True}
                    clients[NICAddress] = True
                    if clientDiff == ({}, []):
                        clients[addr] = True
                        Print(f"{addr} is synced")
                        message = "synced"
                    else:
                        message = (clientDiff, syncedClients := [i for i in clients if clients[i]])
                        
                        Print(f"Sending diff to {addr}:{port}\n{message}")
                        Print("Viable Peers:", syncedClients)
                    safeSend(message, conn)
                    
                    lastStructure = masterStructure
            except Exception as e:
                Print(traceback.format_exc())
                
        
        
if __name__ == '__main__':
    runMaster("./test/another")       
        