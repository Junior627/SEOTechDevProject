import json
import requests
import constants

apikey = constants.api_key
timezone = "America/New_York"

class stockAPI:
    def __init__(self, company, interval, outputsize, startDate, endDate):
        global payload 
        payload = {
                'start_date':startDate,
                'end_date': endDate,
                'symbol':company, 
                'interval':interval, 
                'outputsize':outputsize,
                'timezone':timezone, 
                'apikey':apikey
                }
        
    def requestAPIData(self):
        global r 
        r = requests.get('https://api.twelvedata.com/time_series', params=payload)

    def getDateAndAverage(self):
        # average is x while date is y
        rawdata = r.json()
        global dataDateAverage
        dataDateAverage = {}
        for datapoint in rawdata['values']:
            average = (float(datapoint['high'])+ float(datapoint['low']))/2
            average = round(average, 8)
            dataDateAverage[datapoint['datetime']] = average
        return dataDateAverage

    def printdata(self):
        print("Data")
        print(" ")
        print(json.dumps(r.json(), indent=1))

    def reorderDict(self, dict):
        newDict = {}
        for index in range(len(dict)):
            item = dict.popitem()
            newDict[item[0]] =item[1]
        return newDict

    def significantChange(self):
        global dropDates, belowInflationDates, tenIncreaseDates, orderedData    
        dropDates = {}    
        belowInflationDates = {}
        tenIncreaseDates = {}
        orderedData = {}
        #must not run multiple times, improve
        orderedData = self.reorderDict(dataDateAverage)
        if (len(orderedData) == 0):
            print("Error: Run getDateAndAverage function first")
        for items in orderedData.items():
            if (items[0] == list(orderedData.keys())[-1]):
                continue
            if (items[0] == list(orderedData.keys())[0]):
                previouskey = items[0]
                previousValue = items[1]
                continue
            # stock got lower in value
            if (items[1] < previousValue):
                dropDates[previouskey] = previousValue
            relativeChange = ((items[1]-previousValue)/previousValue)
            # stock growth is lower than inflation
            if (relativeChange < 0.038):
                belowInflationDates[previouskey] = previousValue
            # stock growth greater than 10 percent
            if (relativeChange > 0.1):
                tenIncreaseDates[previouskey] = previousValue

            previouskey = items[0]
            previousValue = items[1]
        
        return dropDates
    def getOrderedDate(self):
        if (len(orderedData) == 0):
            print("Error: Run largestIncrease first")
            return
        return orderedData
    def getDropDates(self):
        return dropDates
    
    def getDropInflationDates(self):
        return belowInflationDates
    
    def gettenincreaseDates(self):
        return tenIncreaseDates
    
    
#Running Class Example

apple = stockAPI("AAPL", "1month", 100, "2015-01-01", "2020-01-01")
apple.requestAPIData()
apple.getDateAndAverage()
apple.significantChange()
print("Stock dropped in value \n")
print(apple.getDropDates())

print("\n Stock growth is below Inflation \n")
print(apple.getDropInflationDates())

print("\n Stock growth is higher than 10 percent \n")
print(apple.gettenincreaseDates())

print("\n Printing entire set \n")
print(apple.getOrderedDate())
