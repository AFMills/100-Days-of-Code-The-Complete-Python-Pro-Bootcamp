from flask import Flask

app = Flask(__name__)       # __name__ denotes the file/module that is currently being run (in this case, __main__)

@app.route('/')                 # Python Decorator; '/' indicates the home route (i.e. the homepage of the site)
def hello_world():
    return '<h1 style="text-align: center">Hello, World!</h1>' \
            '<p>This is a paragraph</p>' \
            '<img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXdxMWxvdzJic2g5MDA5Y3dnMmppb2M5bHlseWNnbmltbDEwbnM3eiZlcD12MV9naWZzX3RyZW5kaW5nJmN0PWc/FY8c5SKwiNf1EtZKGs/giphy.webp">'     # We can use HTML tags in return statements

def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"
    return wrapper

def make_emphasis(function):
    def wrapper():
        return '<em>' + function() + '</em>'
    return wrapper

def make_underlined(function):
    def wrapper():
        return '<u>' + function() + '</u>'
    return wrapper

@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return 'Bye'
    # return '<em><b>Bye</b></em>'

@app.route("/username/<path:name>/<int:number>")
# @app.route("/username/<name>")
def greet(name, number):
    return f"Hello there, {name}! You are {number} years old."

if __name__ == "__main__":
    app.run(debug=True)       # Enables debug mode and automatic refreshing, allowing us to change the server in real-time
                              # You can also access the Flask debugger, which will need the Debugger PIN from the console

# Command Line commands:
#       $env:FLASK_APP="hello.py"
#       flask --app hello run