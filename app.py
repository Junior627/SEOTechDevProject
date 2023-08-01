from flask import Flask, render_template
from stockAPI import filteredData
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def homepage():
    return render_template('home.html', dataset = filteredData)

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/story")
def story():
    return render_template('story.html')


if __name__ == '__main__':
    app.run(debug=True)
