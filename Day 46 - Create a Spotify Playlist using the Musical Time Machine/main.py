import requests
from bs4 import BeautifulSoup

date = input("What date would you like to travel to? Type the date in this format: YYYY-MM-DD\n")

header = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 OPR/127.0.0.0"
}

url = "https://web.archive.org/web/20190920230913/https://www.billboard.com/charts/hot-100/" + date
response = requests.get(url=url, headers=header)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.find_all(name="span", class_="chart-list-item__title-text")
# print(song_names_spans)
song_names = [song.getText().strip() for song in song_names_spans]
# print(song_names)