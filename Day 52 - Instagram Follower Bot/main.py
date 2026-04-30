import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

SIMILAR_ACCOUNT = "chefsteps"
INSTAGRAM_EMAIL = os.environ.get("MY_EMAIL")
INSTAGRAM_PASSWORD = os.environ.get("INSTAGRAM_PASSWORD")

class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(4.2)

        decline_cookies_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"
        cookie_warning = self.driver.find_elements(By.XPATH, decline_cookies_xpath)
        if cookie_warning:
            cookie_warning[0].click()

        username = self.driver.find_element(by=By.XPATH, value='//*[@id="_R_32d9lplcldcpbn6b5ipamH1_"]')
        username.send_keys(INSTAGRAM_EMAIL)

        password = self.driver.find_element(by=By.XPATH, value='//*[@id="_R_33d9lplcldcpbn6b5ipamH1_"]')
        password.send_keys(INSTAGRAM_PASSWORD)

        time.sleep(2.1)
        password.send_keys(Keys.ENTER)

        time.sleep(4.3)

        save_login_prompt = self.driver.find_element(by=By.XPATH, value='//div[contains(text(), "Not now")]')
        if save_login_prompt:
            save_login_prompt.click()

        # time.sleep(3.7)

        # notifications_prompt = self.driver.find_element(by=By.XPATH, value='// button[contains(text(), "Not Now")]')
        # if notifications_prompt:
        #     notifications_prompt.click()

    def find_followers(self):
        # time.sleep(5.2)
        #
        # self.driver.get("https://www.instagram.com/chefsteps/followers/")
        #
        # time.sleep(8.2)
        #
        # modal = self.driver.find_element(by=By.XPATH, value='modal_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]"')
        # for i in range(10):
        #     self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
        #     time.sleep(2)
        pass

    def follow(self):
        pass


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()