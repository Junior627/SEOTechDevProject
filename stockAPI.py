from datetime import datetime
from datetime import date
import json
import requests
import constants
from newsAPI import retrieveDateCompany, requestInfo

apikey = constants.api_key
timezone = "America/New_York"
class stockAPI:
    def __init__(self, company, interval, outputsize, startDate, endDate):
        self.oneRunTime = False
        self.dropDates = {}    
        self.belowInflationDates = {}
        self.tenIncreaseDates = {}
        self.orderedData = {}
        self.dataDateAverage = {}
        self.payload = {
                'start_date':startDate,
                'end_date': endDate,
                'symbol':company, 
                'interval':interval, 
                'outputsize':outputsize,
                'timezone':timezone, 
                'apikey':apikey
                }
        self.r = requests.get('https://api.twelvedata.com/time_series', params=self.payload)

    def getDateAndAverage(self):
        # average is x while date is y
        rawdata = self.r.json()
        for datapoint in rawdata['values']:
            average = (float(datapoint['high'])+ float(datapoint['low']))/2
            average = round(average, 8)
            self.dataDateAverage[datapoint['datetime']] = average
        return self.dataDateAverage

    def printdata(self):
        print("Data")
        print(" ")
        print(json.dumps(self.r.json(), indent=1))

    def reorderDict(self, dict):
        if (self.oneRunTime == True):
            return dict
        newDict = {}
        for index in range(len(dict)):
            item = dict.popitem()
            newDict[item[0]] =item[1]
        self.oneRunTime = True
        return newDict

    def compareDate(self, date1, date2):
        newDate1 = datetime.strptime(date1, "%Y-%m-%d")
        newDate2 = datetime.strptime(date2, "%Y-%m-%d")
        if newDate1 > newDate2:
            return True
        return False

    def significantChange(self):
        self.orderedData = self.reorderDict(self.dataDateAverage)
        if (len(self.orderedData) == 0):
            self.getDateAndAverage()
        for items in self.orderedData.items():
            if (items[0] == list(self.orderedData.keys())[-1]):
                continue
            if (items[0] == list(self.orderedData.keys())[0]):
                previouskey = items[0]
                previousValue = items[1]
                continue
            # stock got lower in value
            if (items[1] < previousValue):
                self.dropDates[previouskey] = previousValue
            relativeChange = ((items[1]-previousValue)/previousValue)
            # stock growth is lower than inflation
            if (relativeChange < 0.038):
                self.belowInflationDates[previouskey] = previousValue
            # stock growth greater than 10 percent
            if (relativeChange > 0.1):
                self.tenIncreaseDates[previouskey] = previousValue

            previouskey = items[0]
            previousValue = items[1]
        
        return self.dropDates
    def getOrderedDate(self):
        if (len(self.orderedData) == 0):
            self.significantChange()
        return self.orderedData
    
    def parseDates(self, dict):
        dateList = list(dict.keys())
        for index in range(len(dateList)):
            dateList[index] = datetime.strptime(dateList[index], "%Y-%m-%d")
        return dateList

    def getdropDates(self):
        return self.parseDates(self.dropDates)
    
    def getDropInflationDates(self):
        return self.parseDates(self.belowInflationDates)
    
    def gettenincreaseDates(self):
        return self.parseDates(self.tenIncreaseDates)
    
    def filterData(self):
        unfilteredData = self.getDateAndAverage()
        global filteredData
        filteredData = []
        for item in unfilteredData.items():
            filteredData.append({"date":item[0],"value":item[1] })
        return filteredData
    
#Running Class Example
def getAPIdata():
    global symbolDate, enddate, filteredData
    requestInfo()
    symbolDate = retrieveDateCompany()
    if int(symbolDate[1]) == 1 or int(symbolDate[1]) == 2:
        startdate =  date(int(symbolDate[2]), int(symbolDate[1])+10, 1)
    else:
        startdate =  date(int(symbolDate[2]), int(symbolDate[1])-2, 1)
    enddate = date(int(symbolDate[2]), int(symbolDate[1]), 1)
    stockData = stockAPI(symbolDate[0], "1day", 100, str(startdate), str(enddate))
    unfilteredData = stockData.getDateAndAverage()
    filteredData = []
    for item in unfilteredData.items():
        filteredData.append({"date":item[0],"value":item[1]})
    

def returnName(name):
    match name:
        case "AMZN":
            return "Amazon"
        case "GOOG":
            return "Google"
        case "AAPL":
            return "Apple"
        case "NVDA":
            return "Nvidia"
        case "MSFT":
            return "Microsoft"
        case "TSLA":
            return "Tesla"
        case _:
            return "Error Check returnName"



# apple = stockAPI("AAPL", "1month", 100, "2015-01-01", "2020-01-01")
# apple.getDateAndAverage()
# apple.significantChange()
# print("Stock dropped in value \n")
# print(apple.getdropDates()[0].year)
# print("\n Stock growth is below Inflation \n")
# print(apple.getDropInflationDates())

# print("\n Stock growth is higher than 10 percent \n")
# print(apple.gettenincreaseDates())

# print("\n Printing entire set \n")
# print(apple.getOrderedDate())
# dataset = apple.getOrderedDate()
