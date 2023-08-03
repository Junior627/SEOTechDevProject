from flask import Flask, render_template
import requests
import random
import pprint

SECRET_KEY = "tEr32X58d79uJx4ez0wtxRgPVni4NbAbPZ3hnPQM" 
symbols = ["TSLA", "AAPL", "MSFT", "GOOG", "AMZN", "NVDA"]
months  = ["01", "02" ,"03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
years = ["2021", "2022"]
bound = 99
newsArray = []

def requestInfo():
    global newsArray 
    newsArray = []

    symbol = randomSelector(symbols)
    month = randomSelector(months)
    year = randomSelector(years)
    print(year)
    url = f"https://api.marketaux.com/v1/news/all?symbols={symbol}&interval=month&published_before={year}-{month}&filter_entities=true&language=en&api_token={SECRET_KEY}"
    response = requests.get(url)
    news = response.json()
    for x in news["data"]:
        newsArray.append(x)
        

def printNews():
    global newsArray
    for x in newsArray:
        print(x['title']+"\n")
        print(x['description']+"\n")

def randomSelector(arr):
    return arr[random.randrange(0, len(arr))]



