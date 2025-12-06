import os, json

class JSONHandling:
    def __init__(self):
        self.settingsFile = "settings.json"
            
        if not os.path.exists(self.settingsFile):
            data = {"color": "Blue", "puzzlePieces": 50}
            with open("settings.json", "w") as f:
                json.dump(data, f)

    def getFileLocation(self):
        return self.settingsFile

    def getDataFull(self):
            try:
                with open(self.settingsFile, "r") as f:
                    return json.load(f)
            except Exception:
                    return {}

    def setData(self, attribute, parameter):
        data = self.getDataFull()
        data[attribute] = parameter
        with open(self.settingsFile, "w") as f:
            json.dump(data, f)

    def getData(self, attribute):
        data = self.getDataFull()
        return data.get(attribute)