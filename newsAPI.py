from flask import Flask, render_template
import requests
import random
import pprint
import constants

SECRET_KEY = constants.news_key 
symbols = ["TSLA", "AAPL", "MSFT", "GOOG", "AMZN", "NVDA"]
months  = ["01", "02" ,"03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
years = ["2021", "2022"]
bound = 99
newsArray = []
symbol=""
Month=""
nextMonth=""
Year=""
nextYear=""
Day="01"

def requestInfo():
    global newsArray 
    newsArray = []

    global symbol
    symbol = randomSelector(symbols)
    global Month
    Month = randomSelector(months)
    global Year
    Year = randomSelector(years)
    getNextDate(Month)
    
    print(Year)
    url = f"https://api.marketaux.com/v1/news/all?symbols={symbol}&interval=month&published_before={Year}-{Month}-{Day}&filter_entities=true&language=en&api_token={SECRET_KEY}"
    response = requests.get(url)
    news = response.json()
    for x in news["data"]:
        newsArray.append(x)
        

def printNews():
    global newsArray
    for x in newsArray:
        print(x['title']+"\n")
        print(x['description']+"\n")

def getNextDate(string):
    Day = "01"
    if string =="12":
        global nextMonth
        nextMonth = "01"
        if Year =="2021":
            global nextYear
            nextYear = "2022"
        elif Year=="2022":
            Day = "30"
        
    else:
        i = 0
        nextYear = Year
        while i < len(months):
            if string == months[i]:
                nextMonth = months[i+1]
            i = i + 1

def randomSelector(arr):
    return arr[random.randrange(0, len(arr))]



