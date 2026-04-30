from flask import Flask
import random

random_number = random.randint(0,9)
print(random_number)

app = Flask(__name__)

@app.route('/')
def home():
    return ('<h1>Guess a number between 0 and 9<h1>'
            '<img src="https://media2.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3MHhoajN5MGw4bmJsZmpvYzY2MWljMDlsOXgwMmRzdnJuczVrdXVtZSZlcD12MV9naWZzX3RyZW5kaW5nJmN0PWc/z4lwT4QTkK3sYITR7Z/giphy.webp">')

@app.route('/<int:guess>')
def guess_number(guess):
    if guess > random_number:
        return ('<h1 style="color: purple">Too High!</h1>'
                '<img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXdxMWxvdzJic2g5MDA5Y3dnMmppb2M5bHlseWNnbmltbDEwbnM3eiZlcD12MV9naWZzX3RyZW5kaW5nJmN0PWc/FY8c5SKwiNf1EtZKGs/giphy.webp">')
    elif guess < random_number:
        return ('<h1 style="color: red">Too Low!</h1>'
                '<img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXdxMWxvdzJic2g5MDA5Y3dnMmppb2M5bHlseWNnbmltbDEwbnM3eiZlcD12MV9naWZzX3RyZW5kaW5nJmN0PWc/xdLH51eNWZAHrwy5mf/200.webp">')
    else:
        return ('<h1 style="color: green">You found me!</h1>'
                '<img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXdxMWxvdzJic2g5MDA5Y3dnMmppb2M5bHlseWNnbmltbDEwbnM3eiZlcD12MV9naWZzX3RyZW5kaW5nJmN0PWc/LPFNd1AJBoYcVUExmE/giphy.webp">')


if __name__ == "__main__":
    app.run(debug=True)