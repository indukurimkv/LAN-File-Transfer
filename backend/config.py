import pickle


if __name__ == "__main__":
    globalConfig = {
        "LANAddress": "192.168.50.90",
        "SourceAddress": "192.168.50.183",
        "SyncDir": "./test/master"
    }

    with open("./global.cfg", "wb") as file:
        pickle.dump(globalConfig, file)
