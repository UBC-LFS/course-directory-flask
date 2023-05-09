from flask import Flask, render_template

from get_course_data import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/test")
def test():
    return "Testing page!"

if __name__ == "__main__":
    app.run(debug=True)