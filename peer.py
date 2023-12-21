from client import sync
from server import runServer
import pickle
from threading import Thread

if __name__ == "__main__":
    with open("./global.cfg", "rb") as file:
        config = pickle.load(file)
    