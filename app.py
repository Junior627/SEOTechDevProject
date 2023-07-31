from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user

import newsAPI


app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY']= '3103cf5454ad2aa0be28c21e7c784e39'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

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
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        remember = True if request.form.get('remember') else False
        if not user:
            flash('Please Sign Up!')
            return render_template('register.html', title='Register', form = form)
        elif user.password != form.password.data:
            flash('Wrong password, please try again')
            return render_template('login.html', title='Register', form = form)
        flash(f'Account created for {form.username.data}!', 'success')
        login_user(user, remember=remember)
        return redirect(url_for('homepage', userName = form.username.data))
    return render_template('login.html', title='Register', form = form)


@app.route("/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already in use')
            return render_template('register.html', title='Register', form = form)
        new_user = User(username = form.username.data, email=form.email.data,password = form.password.data)
        
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('homepage', userName = form.username.data))
    return render_template('register.html', title='Register', form = form)

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")