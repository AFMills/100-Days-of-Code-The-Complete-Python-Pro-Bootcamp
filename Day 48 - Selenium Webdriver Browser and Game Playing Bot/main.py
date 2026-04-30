from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://www.amazon.com/dp/B075CYMYK6?th=1")
driver.get("https://www.python.org")

# price_dollar = driver.find_element(by="class name", value="a-price-whole")
# price_cents = driver.find_element(by="class name", value="a-price-fraction")
# print(f"The price is ${price_dollar.text}.{price_cents.text}")

# search_bar = driver.find_element(by=By.NAME, value="q")
# print(search_bar.tag_name)
# print(search_bar.get_attribute("placeholder"))
# button = driver.find_element(by=By.ID, value="submit")
# print(button.size)
# documentation_link = driver.find_element(by=By.CSS_SELECTOR, value=".documentation-widget a")
# print(documentation_link.text)

# bug_link = driver.find_element(by=By.XPATH, value='//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
# print(bug_link.text)

# driver.find_elements(by=By.CSS_SELECTOR, value="")


# CHALLENGE: Print the event dates on python.org
event_times = driver.find_elements(by=By.CSS_SELECTOR, value=".event-widget time")
event_names = driver.find_elements(by=By.CSS_SELECTOR, value=".event-widget li a")

# events = {}
# for n in range(len(event_times)):
#     events[n] = {
#         "time" : event_times[n].text,
#         "name" : event_names[n].text,
#     }

events = {
    n: {"time": event_times[n].text, "name": event_names[n].text} for n in range(len(event_times))
}

print(events)


# driver.close()        #Closes a single tab
driver.quit()         #Closes all tabs