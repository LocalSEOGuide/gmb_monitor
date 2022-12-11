class GmbLocation: 

    def __init__(self,locationList):
        
        self.output = self.readFile()
        self.index = len(self.output)
        self.input = locationList 

    def addLocation(self): 

        for i in range(len(self.input)):
            temp = {} 
            temp['brand_query'] = self.input[i]['brand_term']
            temp['group_id'] = self.index + 1 
            self.output.append(temp) 

        print(self.output)
        self.saveToFile()

    def readFile(self): 
        if os.path.exists('output.json'):
            with open('output.json', 'r') as openfile:
                return json.load(openfile)
        else:
            return []

    def saveToFile(self):
        with open("output.json", "w") as outfile:
            json.dump(self.output, outfile)
        print("Save output to file!")