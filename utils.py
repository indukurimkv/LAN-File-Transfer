import socket
import pickle

# safeSend and safeRecv must be used as a pair on client and server side!

def safeSend(data, conn: socket.socket, bufferSize=-1, numInitBits = 128):
    output = pickle.dumps(data)
    dataLen = bufferSize if bufferSize > 0 else len(output)
    conn.sendall(f"{dataLen}".ljust(numInitBits).encode())
    conn.sendall(output)

def safeRecv(conn: socket.socket, numInitBits = 128):
    try:
        dataLen = int(conn.recv(numInitBits).decode())
        return pickle.loads(conn.recv(dataLen))
    except Exception as e:
        print(f'Failed to safely Recieve Bytes on {conn.getsockname()[0]}')
        print(e)