from Directories import getStructure, diff
import socket
import pickle

if __name__ == "__main__":
    root = './test/master'
    clients = {}
    
    lastMasterStructure = None
    with socket.create_server(('', 45000)) as sock:
        clients[sock.getsockname()[0]] = True
        
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
                # Desync all clients if changes are made.
                if lastMasterStructure != masterStructure:
                    clients = {sock.getsockname()[0]: True}
                    
                clientDiff = diff(masterStructure, clientStructure)
                if clientDiff == ({}, []):
                    clients[addr] = True
                    print(f"{addr} is synced")
                    message = pickle.dumps("synced")
                else:
                    message = pickle.dumps((clientDiff, [i for i in clients if clients[i]]))
                    print(f"Sending diff to {addr}:\n{message}")
                conn.sendall("{:<128}".format(len(message)).encode())
                conn.sendall(message)
                
                lastMasterStructure = masterStructure
        
        
        
        