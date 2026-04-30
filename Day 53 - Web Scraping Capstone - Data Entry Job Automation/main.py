import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScOo-aKtjj1yrYy9PUr9dv-sXCD7di_yh4MYU17rVZlPmFRRw/viewform?usp=header"

header = {
    "User-Agent" : "CCBot/2.0 (https://commoncrawl.org/faq/)",
    "Accept-Language" : "en-US,en;q=0.5"
}

response = requests.get(url=ZILLOW_URL, headers=header)
data = response.text
soup = BeautifulSoup(data, "html.parser")

all_link_elements = soup.select(".StyledPropertyCardDataWrapper a")     # Create a list of all links on the page using a CSS Selector
all_links = [link["href"] for link in all_link_elements]        # Extract the cleaned URLs
print(f"There are {len(all_links)} links to individual listings in total:")
print(all_links)

all_address_elements = soup.select(".StyledPropertyCardDataWrapper a address")
all_addresses = [address.get_text().replace(" | ", " ").strip() for address in all_address_elements]
print(f"\nAfter having been cleaned up, the {len(all_links)} addresses now look like this:")
print(all_addresses)

all_price_elements = soup.select(".StyledPropertyCardDataWrapper span")
all_prices = [price.get_text().replace("/mo","").split("+")[0] for price in all_price_elements]
print(f"\nAfter having been cleaned up, the {len(all_links)} prices now look like this:")
print(all_prices)



# Use Selenium to fill in the Form

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

for n in range(len(all_links)):
    driver.get(FORM_URL)        #return to form upon submitting at the end of the for loop
    time.sleep(2)

    address = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])

    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_button.click()