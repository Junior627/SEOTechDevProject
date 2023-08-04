from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import constants
from stockAPI import *



app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY']= constants.db_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
score =0
currentuserID = ''
db = SQLAlchemy(app)
migrate = Migrate(app, db)
stockOpen =0
stockClose =0
updatedParams = []

newsDict ={}   

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
        'link1' : newsAPI.newsArray[0]["url"], 
        'link2' : newsAPI.newsArray[1]["url"], 
        'link3' : newsAPI.newsArray[2]["url"]
    }

    return "Updated"
    
@app.route("/")
@app.route("/home")
def homepage():
    stockAPI.getAPIData()
    UpdateStockParams()
    return render_template('home.html', 
                           dataset = stockAPI.filteredData, 
                           change = stockAPI.getFutureData(),
                           pub1 = newsAPI.newsArray[0]["published_at"][:10], 
                           pub2 = newsAPI.newsArray[1]["published_at"][:10], 
                           pub3 = newsAPI.newsArray[2]["published_at"][:10], 
                           title1 = newsAPI.newsArray[0]["title"], 
                           title2 = newsAPI.newsArray[1]["title"], 
                           title3 = newsAPI.newsArray[2]["title"], 
                           disc1 = newsAPI.newsArray[0]["description"], 
                           disc2 = newsAPI.newsArray[1]["description"], 
                           disc3 = newsAPI.newsArray[2]["description"],
                           url1 = newsAPI.newsArray[0]["url"],
                           url2 = newsAPI.newsArray[1]["url"],
                           url3 = newsAPI.newsArray[2]["url"],
                           source1 = newsAPI.newsArray[0]["source"],
                           source2 = newsAPI.newsArray[1]["source"],
                           source3 = newsAPI.newsArray[2]["source"],   
                           company = stockAPI.returnName(stockAPI.symbolDate[0]),

                           stockDateCurrent = stockAPI.rFinal[1]['datetime'],
                           openPriceCurrent = stockAPI.rFinal[1]['open'],
                           closePriceCurrent = stockAPI.rFinal[1]['close'],
                           highPriceCurrent = stockAPI.rFinal[1]['high'],
                           lowPriceCurrent = stockAPI.rFinal[1]['low'],
                           volumeCurrent = stockAPI.rFinal[1]['volume'],

                           stockDateFuture = stockAPI.rFinal[0]['datetime'],
                           openPriceFuture = stockAPI.rFinal[0]['open'],
                           closePriceFuture = stockAPI.rFinal[0]['close'],
                           highPriceFuture = stockAPI.rFinal[0]['high'],
                           lowPriceFuture = stockAPI.rFinal[0]['low'],
                           volumeFuture = stockAPI.rFinal[0]['volume']
                           )

@app.route("/profile")
def profile():
    return render_template('profile.html', dataset = stockAPI.filteredData)

@app.route("/story")
def story():
    return render_template('story.html')

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
    return render_template('home.html',dataset= updatedParams, **newsDict)

@app.route("/LowerCheck")
def CheckStockDiff_L():
    print("worked_L")
    if stockOpen > stockClose:
        UpdateScore()
        print("Correct!")
    else:
        print("Incorrect.")
    homepage()
    return render_template('home.html',dataset= updatedParams, **newsDict)

@app.route("/SameCheck")
def CheckStockDiff_S():
    print("worked_S")
    if stockOpen == stockClose:
        UpdateScore()
        print("Correct!")
    else:
        print("Incorrect.")
    homepage()
    return render_template('home.html',dataset= updatedParams, **newsDict)


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
            return redirect(url_for('homepage', userName = form.username.data))
    return render_template('login.html', title='Register', form = form)

@app.route("/test")
def testFun():
    global currentuserID
    update_user = User.query.filter_by(username=currentuserID).first()
    return render_template('home.html', num =update_user.streakScore)

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
        return redirect(url_for('homepage', userName = form.username.data))
    return render_template('register.html', title='Register', form = form)


def UpdateScore():
    global currentuserID
    update_user = User.query.filter_by(username=currentuserID).first()
    print(update_user)
    update_user.streakScore = update_user.streakScore + 1
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
