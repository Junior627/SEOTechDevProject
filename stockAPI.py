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
        try:
            for datapoint in rawdata['values']:
                average = (float(datapoint['high'])+ float(datapoint['low']))/2
                average = round(average, 8)
                self.dataDateAverage[datapoint['datetime']] = average
        except:
            print(rawdata)
            print("getDateAndAverage Function ")
        return self.dataDateAverage

    def returnJson(self):
        return self.r.json()
    
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
        filteredData = []
        for item in unfilteredData.items():
            filteredData.append({"date":item[0],"value":item[1] })
        return filteredData
    
#Running Class Example
def getAPIData():
    global symbolDate, enddate, filteredData, symbolDate, startDate
    requestInfo()
    symbolDate = retrieveDateCompany()
    if int(symbolDate[1]) == 1:
        startDate =  date(int(symbolDate[2])-1, int(symbolDate[1])+11, 1)
    else:
        startDate =  date(int(symbolDate[2]), int(symbolDate[1])-1, 1)
    enddate = date(int(symbolDate[2]), int(symbolDate[1]), 1)
    stockData = stockAPI(symbolDate[0], "1day", 20, str(startDate), str(enddate))
    return stockData.filterData()

# startDate and endDate specify the interval for the stock graph in the question stage
# once the question is answered, the graph is updated to included a month into the future. That date is endenddate.
def getFutureData():
    global rValues, rMeta
    if int(symbolDate[1]) == 12 or int(symbolDate[1]) == 11:
        endendendDate =  date(int(symbolDate[2])+1, int(symbolDate[1])-10, 1)
    else:
        endendendDate = date(int(symbolDate[2]), int(symbolDate[1])+2, 1)
    payload = {
        'start_date':enddate,
        'end_date': endendendDate,
        'symbol': symbolDate[0], 
        'interval':"1month", 
        'outputsize':2,
        'timezone':timezone, 
        'apikey':apikey
    }
    # r holds the date, open, high, low, close, volume of the set date and a month after the set date
    rFinal = requests.get('https://api.twelvedata.com/time_series', params=payload)
    try:
        rValues = rFinal.json()['values']
        rMeta = rFinal.json()['meta']
        return (float(rValues[0]['close']) - float(rValues[1]['close']))/float(rValues[1]['close'])
    except:
        print("rFinal")
        print("start Date")
        print(enddate)
        print("End Date")
        print(endendendDate)
        print(rValues.json())
    

def getFutureDetails():
    if int(symbolDate[1]) == 12:
        endendDate =  date(int(symbolDate[2])+1, int(symbolDate[1])-11, 1)
    else:
        endendDate = date(int(symbolDate[2]), int(symbolDate[1])+1, 1)
    stockParams = stockAPI(symbolDate[0], "1day", 60, startDate, endendDate)
    print("rFinal")
    print("start Date")
    print(startDate)
    print("End Date")
    print(enddate)
    print("End END Date")
    print(endendDate)
    return stockParams.filterData()

def returnName(name, shorten):
    match name:
        case "AMZN":
            if (shorten == 1): return "Amazon"
            return "Amazon.com, Inc"
        case "GOOG":
            if(shorten == 1): return "Google"
            return "Alphabet Inc"
        case "AAPL":
            if(shorten == 1): return "Apple"
            return "Apple Inc"
        case "NVDA":
            if(shorten == 1): return "Nvidia"
            return "NVIDIA Corp"
        case "MSFT":
            if(shorten == 1): return "Microsoft"
            return "Microsoft Corp"
        case "TSLA":
            if(shorten == 1): return "Tesla"
            return "Tesla Inc"
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
