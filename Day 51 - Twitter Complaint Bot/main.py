import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import os
import time

# from requests_oauthlib import OAuth1

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = ""
TWITTER_EMAIL = os.environ.get("MY_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")

# auth = OAuth1(API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(3)

        go_button =self.driver.find_element(by=By.CSS_SELECTOR, value=".start-button a")
        go_button.click()
        time.sleep(60)

        self.down = self.driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        self.up = self.driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text

        print(f"Download speed: {self.down}")
        print(f"Upload speed: {self.up}")

    def tweet_at_provider(self):
        # self.driver.get("https://api.x.com")
        # payload = {
        #     "text": f"Hey ISP! Why is my internet speed {self.down}🔻/{self.up}🔺 "
        #             f"when I am paying for {PROMISED_DOWN}🔻/{PROMISED_UP}🔺? "
        #             f"Link: https://www.speedtest.net/result/{self.test_id}."
        # }
        # response = requests.post("https://api.x.com", json=payload, auth=auth)
        # print(response.json())
        pass





bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()