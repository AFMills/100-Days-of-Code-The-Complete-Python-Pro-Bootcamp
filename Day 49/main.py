import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = "AppBrewery2192026"

# Have Chrome stay open upon running code
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Give Selenium its own user profile
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")     # Create a directory in project folder to store Chrome profile info with
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")     #Tell the Chrome driver to store the profile info

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://appbrewery.github.io/gym/")


# ------------ AUTOMATED LOGIN ------------
wait = WebDriverWait(driver, 2)         # Alternative to time.sleep()

login_button = wait.until(expected_conditions.element_to_be_clickable((By.ID, "login-button")))
login_button.click()

email_input = wait.until(expected_conditions.presence_of_element_located((By.ID, "email-input")))
# email_input = driver.find_element(by=By.ID, value="email-input")
email_input.clear()         # Clear the text in the text input field
email_input.send_keys(MY_EMAIL)

password_input = driver.find_element(by=By.ID, value="password-input")
password_input.clear()
password_input.send_keys(MY_PASSWORD)

submit_button = driver.find_element(by=By.ID, value="submit-button")
submit_button.click()

wait.until(expected_conditions.presence_of_element_located((By.ID, "schedule-page")))


# ------------ BOOK A CLASS ------------
class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

# ------------ ADD COUNTERS ------------
booked_count = 0
waitlist_count = 0
already_booked_count = 0

# ------------ BOOK EVERY TUES AND THURS CLASS AND PRINT DETAILED LIST ------------
processed_classes = []

for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    if "Tue" in day_title or "Thu" in day_title:
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time_text:
            class_name = card.find_element(by=By.CSS_SELECTOR, value="h3[id^='class-name-']").text  # Get the class name
            book_button = card.find_element(by=By.CSS_SELECTOR, value="button[id^='book-button-']")
            
            class_details = f"{class_name} on {day_title}"
            
            # ------------ CHECK IF ALREADY BOOKED ------------
            if book_button.text == "Booked":
                print(f"Already booked: {class_details}")
                already_booked_count += 1
                processed_classes.append(f"[Booked] {class_details}")
            elif book_button.text == "Waitlisted":
                print(f"Already on waitlist: {class_details}")
                already_booked_count += 1
                processed_classes.append(f"[Waitlisted] {class_details}")
            elif book_button.text == "Book Class":
                book_button.click()
                print(f"Successfully Booked: {class_details}")
                booked_count += 1
                processed_classes.append(f"[New Booking] {class_details}")
                time.sleep(0.5)
            elif book_button.text == "Join Waitlist":
                book_button.click()
                print(f"Joined waitlist: {class_details}")
                waitlist_count += 1
                processed_classes.append(f"[New Waitlist] {class_details}")
                time.sleep(0.5)

# print("\n--- BOOKING SUMMARY ---")
# print(f"Classes booked: {booked_count}")
# print(f"Waitlists joined: {waitlist_count}")
# print(f"Already booked/waitlisted: {already_booked_count}")
# print(f"Total Tuesday & Thursday 6pm classes processed: {booked_count + waitlist_count + already_booked_count}")
#
# print("\n--- DETAILED CLASS LIST ---")
# for class_detail in processed_classes:
#     print(f"  • {class_detail}")



# ------------ VERIFY BOOKINGS ------------

total_booked = already_booked_count + booked_count + waitlist_count
print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_booked} ---")
print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")

# Navigate to My Bookings page
my_bookings_link = driver.find_element(By.ID, "my-bookings-link")
my_bookings_link.click()

# Wait for My Bookings page to load
wait.until(expected_conditions.presence_of_element_located((By.ID, "my-bookings-page")))

# Count all Tuesday/Thursday 6pm bookings
verified_count = 0

# Find ALL booking cards (both confirmed and waitlist)
all_cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")

for card in all_cards:
    try:
        when_paragraph = card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
        when_text = when_paragraph.text

        # Check if it's a Tuesday or Thursday 6pm class
        if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
            class_name = card.find_element(By.TAG_NAME, "h3").text
            print(f"  ✓ Verified: {class_name}")
            verified_count += 1
    except NoSuchElementException:
        # Skip if no "When:" text found (not a booking card)
        pass

# Simple comparison
print(f"\n--- VERIFICATION RESULT ---")
print(f"Expected: {total_booked} bookings")
print(f"Found: {verified_count} bookings")

if total_booked == verified_count:
    print("SUCCESS: All bookings verified!")
else:
    print(f"MISMATCH: Missing {total_booked - verified_count} bookings")
