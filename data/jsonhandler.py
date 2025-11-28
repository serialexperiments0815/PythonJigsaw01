import os, json

class JSONHandling:
    def __init__(self):
        if os.path.exists("settings.json"):
            self.settingsFile = "settings.json"
        else:
            data = {"color": "Blue", "puzzlePieces": 50}
            with open("settings.json", "w") as f:
                json.dump(data, f)

    def getFileLocation(self):
        return self.settingsFile

    def getDataFull(self):
        if os.path.exists("settings.json"):
            try:
                with open(self.settingsFile) as f:
                    rValue = json.load(f)
                    return rValue
            except Exception:
                pass

    def setData(self, attribute, parameter):
        data = self.getDataFull()
        data[attribute] = parameter
        with open(self.settingsFile, "w") as f:
            json.dump(data, f)

    def getData(self, attribute):
        data = self.getDataFull()
        return data[attribute]