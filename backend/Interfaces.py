import psutil
import pickle

def getInterfaces():
    interfaceInfo = psutil.net_if_addrs()
    out = {}
    for interface in interfaceInfo:
        mac = ''
        ip = ''
        for address in interfaceInfo[interface]:
            if address.family == psutil.AF_LINK:
                mac = address.address
            if address.family == 2:
                ip = address.address
        out[interface] = (mac, ip)
    return out
def confToIp(confKey, path):
    with open(path, "rb") as file:
        interfaceName, mac = pickle.load(file)[confKey]
    
    interfaceInfo = psutil.net_if_addrs()
    for interface in interfaceInfo:
        currMac = ''
        currIp = ''
        for address in interfaceInfo[interface]:
            if address.family == -1:
                currMac = address.address
            if address.family == 2:
                currIp = address.address
        if currMac == mac and interface == interfaceName:
            return currIp
                

if __name__ == "__main__":
    print(confToIp("LANAddress", "./global.cfg"))