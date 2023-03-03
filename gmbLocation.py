import os
import json


class GmbLocation:

    def __init__(self):

        self.output = []
        self.index = len(self.output)

    #  function to add location inputs.
    def addLocation(self, locationList):
        self.remove()
        self.output.append(locationList)
        self.saveToFile()  # save input as json file to local machine

    # function to scan json file from local machine and return contents 
    # it will be called every time the class initiated 
    def readFile(self):
        if os.path.exists('output.json'):
            with open('output.json', 'r') as openfile:
                return json.load(openfile)
        else:
            return []

    # function to save new list into json file 
    def saveToFile(self):
        with open("output.json", "w") as outfile:
            json.dump(self.output, outfile)
        print("Save output to file!")

    # function to remove content from file
    def remove(self):
        self.output = []
        self.saveToFile()  # save input as json file to local machine
