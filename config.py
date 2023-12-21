import pickle


if __name__ == "__main__":
    globalConfig = {
        "LANAddress": "127.0.0.1",
        "SourceAddress": "127.0.0.1",
        "SyncDir": "./test"
    }
    
    with open("./global.cfg", "wb") as file:
        pickle.dump(globalConfig, file)
