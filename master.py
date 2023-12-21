from Directories import getStructure, diff
import socket
import pickle

if __name__ == "__main__":
    root = './test/master'
    clients = {}
    NICAddress = '192.168.50.183'
    
    with socket.create_server(('', 45000)) as sock:
        clients[NICAddress] = True
        lastStructure = None
        
        sock.listen()
        while True:
            conn, (addr, port) = sock.accept()
            print(f"connected to {addr}")
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
                    print(f"{addr} is synced")
                    message = pickle.dumps("synced")
                else:
                    message = pickle.dumps((clientDiff,
                                            syncedClients := [i for i in clients if clients[i]]))
                    print(f"Sending diff to {addr}:\n{message}")
                    print("Viable Peers:", syncedClients)
                conn.sendall("{:<128}".format(len(message)).encode())
                conn.sendall(message)
                
                lastStructure = masterStructure
                
        
        
        
        