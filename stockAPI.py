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
        data = {}
        for datapoint in rawdata['values']:
            average = (float(datapoint['high'])+ float(datapoint['low']))/2
            average = round(average, 8)
            data[datapoint['datetime']] = average
        return data

    def printdata(self):
        print("Data")
        print(" ")
        print(json.dumps(r.json(), indent=1))


#Running Class Example

apple = stockAPI("AAPL", "1week", 10, "2015-01-01", "2020-01-01")
apple.requestAPIData()
print(apple.getDateAndAverage())
