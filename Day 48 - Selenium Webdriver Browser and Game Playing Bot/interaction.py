from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# driver.get("https://en.wikipedia.org")
# number_of_articles = driver.find_element(by=By.XPATH, value='//*[@id="articlecount"]/ul/li[2]/a[1]')
# # number_of_articles = driver.find_element(By.CSS_SELECTOR, "#articlecount li:nth-of-type(2) a")
# # print(number_of_articles.text)
# # number_of_articles.click()
#
# # # Find element by link text
# # all_portals = driver.find_element(by=By.LINK_TEXT, value="Content portals")
# # all_portals.click()
#
# # Find the "Search" <input> by Name
# search = driver.find_element(by=By.NAME, value="search")
# # search.send_keys("Python")
#
# # Sending keyboard input to Selenium
# search.send_keys("Python", Keys.ENTER)


# CHALLENGE: Fill out a form
driver.get("https://secure-retreat-92358.herokuapp.com")

fname = driver.find_element(by=By.NAME, value="fName")
fname.send_keys("Dexter")

lname = driver.find_element(by=By.NAME, value="lName")
lname.send_keys("Grif")

email = driver.find_element(by=By.NAME, value="email")
email.send_keys("caleb@achievementhunter.com")



# driver.close()