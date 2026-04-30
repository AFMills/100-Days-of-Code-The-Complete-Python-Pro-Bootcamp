from bs4 import BeautifulSoup
import requests
import smtplib
import os

# url = "https://appbrewery.github.io/instant_pot/"
url = "https://www.amazon.com/dp/B075CYMYK6?th=1"

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
    "X-Amzn-Trace-Id": "Root=1-686a92b7-37ea2cf169bbd9e75bd5a664"
}

response = requests.get(url=url, headers=header)

soup = BeautifulSoup(response.text, "html.parser")

price = soup.find(class_="a-offscreen").getText()
print(price)
price_as_float = float(price.split("$")[1])
print(price_as_float)


# ================ SEND AN EMAIL ================

MAX_PRICE = 100
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_EMAIL_PASSWORD")


title = soup.find(name="span", id="productTitle").get_text().strip()
print(title)

if price_as_float < MAX_PRICE:
    message = f"{title} is on sale for {price}!"

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject:Low Price Alert!\n\n{message}\n{url}".encode("utf-8"))
