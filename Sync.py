from peer import peer
from source import source
import pickle

if __name__ == "__main__":
    with open('./global.cfg', 'rb') as file:
        config = pickle.load(file)
        if config["isSource"]: source(config)
        else: peer(config)