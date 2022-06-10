import json

class keyPackage:
    def getKeys(self):
        file = open("settings/variables.json", encoding="UTF-8")
        jsonLoaded = json.load(file)
        return jsonLoaded["keys"]