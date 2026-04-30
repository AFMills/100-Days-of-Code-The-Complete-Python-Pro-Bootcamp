from flask import Flask
import random

app = Flask(__name__)       # __name__ denotes the file/module that is currently being run (in this case, __main__)

# print(random.__name__)
# print(__name__)

@app.route("/")                 # Python Decorator; '/' indicates the home route (i.e. the homepage of the site)
def hello_world():              # The decorator makes it so that hello_world() only runs on the homepage ("/")
    return "<p>Hello, World!</p>"

@app.route("/bye")
def say_bye():
    return "Bye"

if __name__ == "__main__":
    app.run()       # Effectively works the same as entering "flask run" in the terminal

# $env:FLASK_APP="hello.py"
# flask --app hello run