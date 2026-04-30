from flask import Flask, render_template
import random
import datetime
import requests

app = Flask(__name__)

@app.route('/')
def home():
    random_number = random.randint(1,10)
    current_year = datetime.datetime.now().year
    return render_template("index.html", num=random_number, year=current_year)     # We can pass over any value we want using kwargs (in this case, num and year)

@app.route('/guess/<name>')
def guess(name):
    gender_url = f'https://api.genderize.io?name={name}'
    gender_response = requests.get(gender_url)
    gender_data = gender_response.json()
    gender = gender_data["gender"]

    age_url = 'https://api.agify.io?name=michael'
    age_response = requests.get(age_url)
    age_data = age_response.json()
    age = age_data["age"]

    return render_template("guess.html", person_name=name, person_gender=gender, person_age=age)

@app.route('/blog/<num>')
def get_blog(num):
    print(num)
    blog_url = 'https://api.npoint.io/c790b4d5cab58020d391'
    blog_response = requests.get(blog_url)
    all_posts = blog_response.json()
    return render_template("blog.html", posts=all_posts)

if __name__ == "__main__":
    app.run(debug=True)