from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def homepage():
    return render_template('home.html')

@app.route("/profile")
def story():
    return render_template('profile.html')

@app.route("/story")
def story():
    return render_template('story.html')


if __name__ == '__main__':
    app.run(debug=True)
