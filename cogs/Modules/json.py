import json

def readJSONFile(folder, filename):
    with open("./" + folder + "/" + filename) as json_file:
        data = json.load(json_file)

    return data

def writeJSONFile(folder, filename, data):
    with open("./" + folder + "/" + filename, 'w') as outfile:
        json.dump(data, outfile)