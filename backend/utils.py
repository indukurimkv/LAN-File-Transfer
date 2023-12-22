import socket
import pickle

def recieveAll(numBytes , conn):
    out = b''
    recievedBytes = 0
    while recievedBytes < numBytes:
        out += conn.recv(numBytes - recievedBytes)
        recievedBytes += len(out)
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