class GmbLocation: 

    def __init__(self,locationList):
        
        self.output = self.readFile() # scan json file from local machine
        self.index = len(self.output)
        self.input = locationList 

    # function to add location inputs. 
    def addLocation(self): 

        for i in range(len(self.input)):
            temp = {} 
            temp['brand_query'] = self.input[i]['brand_term']
            temp['group_id'] = self.index + 1 
            self.output.append(temp) 
        self.saveToFile() # save input as json file to local machine 

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