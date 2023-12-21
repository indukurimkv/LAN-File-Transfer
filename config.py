import pickle


if __name__ == "__main__":
    globalConfig = {
        "LANAddress": "127.0.0.1"
    }
    with open("./global.cfg", "wb") as file:
        pickle.dump(globalConfig, file)
