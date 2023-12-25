from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

# Set up the WebDriver (in this case, we'll use Chrome)
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # Run Chrome in headless mode (hidden browser)
driver = webdriver.Chrome(options=options)
#driver2 = webdriver.Chrome()

# Navigate to Google
driver.get("https://www.google.com")


# Find the search box and enter the search term
search_box = driver.find_element("name", "q")  # The name attribute of the Google search box is "q"
search_term = "north andover" + " robotevents over under 2023-24"
division_name = "division-1"
search_box.send_keys(search_term)
search_box.send_keys(Keys.RETURN)  # Press Enter to perform the search

# Wait for the search results to load (you may need to adjust the sleep duration or use WebDriverWait)
driver.implicitly_wait(5)

result = driver.find_element(By.TAG_NAME,'h3')
result.click()
driver.implicitly_wait(5)

# Get the current URL (this will be the URL of the page you've navigated to)
current_url = driver.current_url
print("Current URL:", current_url)
driver.implicitly_wait(5)

if "/es/" in current_url:
    resultsUrl = current_url[:28] + current_url[31:]
resultsUrl = resultsUrl + "#" + division_name

print(resultsUrl)
time.sleep(2)
driver.get(resultsUrl)
driver.implicitly_wait(5)
time.sleep(3)

'''
try:
    skills_button = driver.find_element(By.CSS_SELECTOR, "active nav-link")
    next_button = skills_button.find_element(By.XPATH, 'following-sibling::button')
    next_button.click()
except Exception as e:
    print(f"Buttons not found: {e}")
'''

time.sleep(5)
#result.click()

# Close the browser
driver.quit()