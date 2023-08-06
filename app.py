from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import newsAPI
import constants
from datetime import datetime
import newsAPI
import stockAPI



app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY']= constants.db_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

score = 0
currentuserID = ''
db = SQLAlchemy(app)
migrate = Migrate(app, db)
stockOpen =0
stockClose =0
updatedParams = []

newsDict ={}   
userDict ={
    'dbUser' : "",
    'dbStreak' : 0
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    streakScore = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

with app.app_context():
    db.create_all()

@app.route("/news")
def newsTrial():
    global newsDict
    newsDict={}
    newsDict={
        'symbol': newsAPI.newsArray[0]["entities"][0]["name"],
        'pub1': newsAPI.newsArray[0]["published_at"], 
        'pub2' : newsAPI.newsArray[1]["published_at"], 
        'pub3' : newsAPI.newsArray[2]["published_at"], 
        'title1' : newsAPI.newsArray[0]["title"], 
        'title2' : newsAPI.newsArray[1]["title"], 
        'title3' : newsAPI.newsArray[2]["title"], 
        'disc1' : newsAPI.newsArray[0]["description"], 
        'disc2' : newsAPI.newsArray[1]["description"], 
        'disc3' : newsAPI.newsArray[2]["description"],
        'url1' : newsAPI.newsArray[0]["url"], 
        'url2' : newsAPI.newsArray[1]["url"], 
        'url3' : newsAPI.newsArray[2]["url"],
        'source1' : newsAPI.newsArray[0]["source"],
        'source2' : newsAPI.newsArray[1]["source"],
        'source3' : newsAPI.newsArray[2]["source"],  
    }

    return "Updated"

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        print(user)
        if not user:
            print('Please Sign Up!')
            return redirect(url_for('register', title='Register', form = form))
        elif user.password != form.password.data:
            print('Wrong password, please try again')
            return render_template('login.html', title='Register', form = form)
        else:
            global currentuserID
            currentuserID = user.username
            print(currentuserID)
            print(f'Logged In Successful, {form.username.data}!')
            displayUserInfo(user.username, user.streakScore)
            return redirect(url_for('homepage', userName = form.username.data))
    return render_template('login.html', title='Register', form = form)

@app.route("/signup", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user:
            print('Email address already in use')
            return render_template('register.html', title='Register', form = form)
        user_name = User.query.filter_by(username=form.username.data).first()
        if user_name:
            print('Username already taken')
            return render_template('register.html', title='Register', form = form)
        new_user = User(username = form.username.data, email=form.email.data,password = form.password.data, streakScore = 0)
        global currentuserID
        db.session.add(new_user)
        currentuserID = new_user.username
        print(currentuserID)
        db.session.commit()
        print(f'Account created for {form.username.data}!', 'success')
        print(f"{new_user.password}")
        print(f"{new_user.streakScore}")
        displayUserInfo(new_user.username, 0)
        return redirect(url_for('homepage', userName = form.username.data))
    return render_template('register.html', title='Register', form = form)

@app.route("/stocksUpdate")
def UpdateStockParams():
    global stockClose
    global stockOpen
    global stockParams
    global updatedParams

    newsAPI.requestInfo()
    startDate = newsAPI.Year+"-"+newsAPI.Month+"-01"
    endDate = newsAPI.nextYear+"-"+newsAPI.nextMonth+"-01"
    print(startDate)
    print(endDate)
    print(newsAPI.symbol)
    stockParams = stockAPI(newsAPI.symbol, "1day", 100, startDate, endDate)
    print(stockParams)
    updatedParams = stockParams.filterData()
    print(updatedParams)
    newsTrial()

    stockClose= float(updatedParams[0]["value"])
    stockOpen = float(updatedParams[len(updatedParams)-1]["value"])
    print(stockOpen)
    print(stockClose)
    return("Updated")

@app.route("/HigherCheck")
def CheckStockDiff_H():
    if stockOpen < stockClose:
        UpdateScore()
        print("Correct!")
    else:
        print("Incorrect.")
    homepage()
    return render_template('home.html', loggedUser = userDict['dbUser'], loggedScore = userDict['dbStreak'], **newsDict,
                                            dataset = filteredData, 
                                            change = stockAPI.getFutureData(),
                                            updatedDataset = stockAPI.getFutureDetails(),

                                            company = stockAPI.returnName(stockAPI.symbolDate[0], 1),
                                            companyLong = stockAPI.returnName(stockAPI.symbolDate[0], 0),
                                            stockType = stockAPI.rMeta['type'], 

                                            stockDateCurrent = stockAPI.rValues[1]['datetime'],
                                            openPriceCurrent = round(float(stockAPI.rValues[1]['open']),2),
                                            closePriceCurrent = round(float(stockAPI.rValues[1]['close']),2),
                                            highPriceCurrent = round(float(stockAPI.rValues[1]['high']),2),
                                            lowPriceCurrent = round(float(stockAPI.rValues[1]['low']),2),
                                            volumeCurrent = round(float(stockAPI.rValues[1]['volume']),3),

                                            stockDateFuture = stockAPI.rValues[0]['datetime'],
                                            openPriceFuture = round(float(stockAPI.rValues[0]['open']),2),
                                            closePriceFuture = round(float(stockAPI.rValues[0]['close']),2),
                                            highPriceFuture = round(float(stockAPI.rValues[0]['high']),2),
                                            lowPriceFuture = round(float(stockAPI.rValues[0]['low']),2),
                                            volumeFuture = round(float(stockAPI.rValues[0]['volume']),3)
                           )

@app.route("/LowerCheck")
def CheckStockDiff_L():
    print("worked_L")
    if stockOpen > stockClose:
        UpdateScore()
        print("Correct!")
    else:
        print("Incorrect.")
    homepage()
    return render_template('home.html',  loggedUser = userDict['dbUser'], loggedScore = userDict['dbStreak'], **newsDict,
                                            dataset = filteredData, 
                                            change = stockAPI.getFutureData(),
                                            updatedDataset = stockAPI.getFutureDetails(),

                                            company = stockAPI.returnName(stockAPI.symbolDate[0], 1),
                                            companyLong = stockAPI.returnName(stockAPI.symbolDate[0], 0),
                                            stockType = stockAPI.rMeta['type'], 

                                            stockDateCurrent = stockAPI.rValues[1]['datetime'],
                                            openPriceCurrent = round(float(stockAPI.rValues[1]['open']),2),
                                            closePriceCurrent = round(float(stockAPI.rValues[1]['close']),2),
                                            highPriceCurrent = round(float(stockAPI.rValues[1]['high']),2),
                                            lowPriceCurrent = round(float(stockAPI.rValues[1]['low']),2),
                                            volumeCurrent = round(float(stockAPI.rValues[1]['volume']),3),

                                            stockDateFuture = stockAPI.rValues[0]['datetime'],
                                            openPriceFuture = round(float(stockAPI.rValues[0]['open']),2),
                                            closePriceFuture = round(float(stockAPI.rValues[0]['close']),2),
                                            highPriceFuture = round(float(stockAPI.rValues[0]['high']),2),
                                            lowPriceFuture = round(float(stockAPI.rValues[0]['low']),2),
                                            volumeFuture = round(float(stockAPI.rValues[0]['volume']),3)
                           )

@app.route("/SameCheck")
def CheckStockDiff_S():
    print("worked_S")
    if stockOpen == stockClose:
        UpdateScore()
        print("Correct!")
    else:
        print("Incorrect.")
    homepage()
    return render_template('home.html',  loggedUser = userDict['dbUser'], loggedScore = userDict['dbStreak'], **newsDict,
                                            dataset = filteredData, 
                                            change = stockAPI.getFutureData(),
                                            updatedDataset = stockAPI.getFutureDetails(),

                                            company = stockAPI.returnName(stockAPI.symbolDate[0], 1),
                                            companyLong = stockAPI.returnName(stockAPI.symbolDate[0], 0),
                                            stockType = stockAPI.rMeta['type'], 

                                            stockDateCurrent = stockAPI.rValues[1]['datetime'],
                                            openPriceCurrent = round(float(stockAPI.rValues[1]['open']),2),
                                            closePriceCurrent = round(float(stockAPI.rValues[1]['close']),2),
                                            highPriceCurrent = round(float(stockAPI.rValues[1]['high']),2),
                                            lowPriceCurrent = round(float(stockAPI.rValues[1]['low']),2),
                                            volumeCurrent = round(float(stockAPI.rValues[1]['volume']),3),

                                            stockDateFuture = stockAPI.rValues[0]['datetime'],
                                            openPriceFuture = round(float(stockAPI.rValues[0]['open']),2),
                                            closePriceFuture = round(float(stockAPI.rValues[0]['close']),2),
                                            highPriceFuture = round(float(stockAPI.rValues[0]['high']),2),
                                            lowPriceFuture = round(float(stockAPI.rValues[0]['low']),2),
                                            volumeFuture = round(float(stockAPI.rValues[0]['volume']),3)
                           )

@app.route("/update")
def UpdateScore():
    global score
    score = score + 1
    global currentuserID
    update_user = User.query.filter_by(username=currentuserID).first()
    if update_user:
        if score > update_user.streakScore:
            update_user.streakScore = update_user.streakScore + 1
            db.session.commit()
            displayUserInfo(update_user.username, update_user.streakScore)
    return("Updated")

@app.route("/home")    
@app.route("/")
def homepage():
    filteredData  = stockAPI.getAPIData()
    newsTrial()
    return render_template('home.html',  loggedUser = userDict['dbUser'], loggedScore = userDict['dbStreak'], **newsDict,
                                            dataset = filteredData, 
                                            change = stockAPI.getFutureData(),
                                            updatedDataset = stockAPI.getFutureDetails(),

                                            company = stockAPI.returnName(stockAPI.symbolDate[0], 1),
                                            companyLong = stockAPI.returnName(stockAPI.symbolDate[0], 0),
                                            stockType = stockAPI.rMeta['type'], 

                                            stockDateCurrent = stockAPI.rValues[1]['datetime'],
                                            openPriceCurrent = round(float(stockAPI.rValues[1]['open']),2),
                                            closePriceCurrent = round(float(stockAPI.rValues[1]['close']),2),
                                            highPriceCurrent = round(float(stockAPI.rValues[1]['high']),2),
                                            lowPriceCurrent = round(float(stockAPI.rValues[1]['low']),2),
                                            volumeCurrent = round(float(stockAPI.rValues[1]['volume']),3),

                                            stockDateFuture = stockAPI.rValues[0]['datetime'],
                                            openPriceFuture = round(float(stockAPI.rValues[0]['open']),2),
                                            closePriceFuture = round(float(stockAPI.rValues[0]['close']),2),
                                            highPriceFuture = round(float(stockAPI.rValues[0]['high']),2),
                                            lowPriceFuture = round(float(stockAPI.rValues[0]['low']),2),
                                            volumeFuture = round(float(stockAPI.rValues[0]['volume']),3)
                           )

@app.route("/profile")
def profile():
    return render_template('profile.html', dataset = stockAPI.filteredData)

@app.route("/story")
def story():
    return render_template('story.html')

def formatDate(date):
    newDate = datetime.strptime(date, "%Y-%m-%d")
    return "" + newDate.strftime("%B") + " " + newDate.strftime("%d")+ ", " + newDate.strftime("%Y")

def displayUserInfo(name , streak):
    global userDict
    userDict ={
        'dbUser': name,
        'dbStreak': streak
    }
    
if __name__ == '__main__':
    app.run(debug=True)
