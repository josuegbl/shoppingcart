import json

class CheckoutClass:
    def __init__(self, jsonPrices, jsonDiscounts):
        self.itemPrices = jsonPrices
        self.discounts = jsonDiscounts
        self.scannedItems = self._getItemsNames()
    
    def scan(self, item):
        """get the item name and fill the dictionary
        with amount of all items."""
        self.scannedItems[item] += 1
        
    def total(self):
        dictPrices = self._dictPrices()
        scItemsList, total = self._applyDiscounts()
        for k,v in zip(dictPrices.items(), scItemsList):
            total += k[1]*v
        print("total amount: %0.2f € " %total)

    def resetScan(self):
        """Function to reset the scanned items."""
        self.scannedItems = self._getItemsNames()
    
    def _dictPrices(self):
        with open(self.itemPrices) as f:
            return json.load(f)

    def _getItemsNames(self):
        """get the items names and generates a dictionary
        to store the number of items."""
        with open(self.itemPrices) as f:
            data = json.load(f)
        return dict((k, 0) for k, v in data.items())

    def _getDiscounts(self):
        with open(self.discounts) as f:
            return json.load(f)

    def _applyDiscounts(self, total=0):
        """function to apply the discounts availables on json file.
        The priority order is given by the json file, i.e first 
        discount to apply is the upper one in the json file."""
        
        scItemsList = self._listFromDict(self.scannedItems)
        dictDiscounts = self._getDiscounts()
        for k,v in dictDiscounts.items():
            discItemsDict = self._getItemsNames()
            for i in v["items"]:
                discItemsDict[i]+= 1
            discList = self._listFromDict(discItemsDict)
            while all(i-j>-1 for i,j in zip(scItemsList, discList)):
                if v["ppunit"] == "false":
                    scItemsList = [i-j for i,j in zip(scItemsList, discList)]
                    total += v["price"]
                else:
                    length = len(scItemsList)
                    for l,i,j in zip(range(length), scItemsList, discList):
                        if j > 0:
                            total += v["price"]*i
                            scItemsList[l] = 0
        return scItemsList, total

    def _listFromDict(self, dct):
        return [v for k,v in dct.items()]
