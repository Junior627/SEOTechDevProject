from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from stockAPI import filteredData

import newsAPI


app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY']= 'b5e8834370808fe7be05c5ae699014e4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
i =0
currentuserID = ''
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
    newsAPI.requestInfo()
    return render_template('NewsBlock.html', symbol = newsAPI.newsArray[0]["entities"][0]["name"] , pub1 =newsAPI.newsArray[0]["published_at"], pub2 = newsAPI.newsArray[1]["published_at"], pub3 = newsAPI.newsArray[2]["published_at"], title1 = newsAPI.newsArray[0]["title"], title2= newsAPI.newsArray[1]["title"], title3= newsAPI.newsArray[2]["title"], disc1 = newsAPI.newsArray[0]["description"], disc2 = newsAPI.newsArray[1]["description"], disc3  = newsAPI.newsArray[2]["description"] )
@app.route("/home")
def homepage():
    return render_template('home.html', dataset = filteredData)

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/story")
def story():
    return render_template('story.html')


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

@app.route("/", methods=['GET', 'POST'])
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