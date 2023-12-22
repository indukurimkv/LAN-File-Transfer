import socket
import pickle

# Return numBytes bytes from buffer. 
# onRecieve callback can perform operations on recieved bytes.
def recieveAll(numBytes: int, conn: socket.socket, onRecieve = None):
    out = b''
    numRecievedBytes = 0
    while numRecievedBytes < numBytes:
        recievedBytes = conn.recv(numBytes - numRecievedBytes)
        numRecievedBytes += len(recievedBytes)
        if onRecieve != None:
            onRecieve(recievedBytes)
        else:
            out += recievedBytes
    return out

# safeSend and safeRecv must be used as a pair on client and server side!

def safeSend(data, conn: socket.socket, bufferSize=-1, numInitBits = 128):
    output = pickle.dumps(data)
    dataLen = bufferSize if bufferSize > 0 else len(output)
    conn.sendall(f"{dataLen}".ljust(numInitBits).encode())
    conn.sendall(output)

def safeRecv(conn: socket.socket, numInitBits = 128):
    try:
        dataLen = int(recieveAll(numInitBits, conn).decode())
        return pickle.loads(recieveAll(dataLen, conn))
            
    except Exception as e:
        print(f'Failed to safely Recieve Bytes on {conn.getsockname()[0]}')
        print(e)