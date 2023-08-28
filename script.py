import re
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# Path to ShareX's History.json file
history_file_path = "../Documents/ShareX/History.json"  # Replace with the correct path
count = 0

# Read the entire file content
with open(history_file_path, "r", encoding="utf-8") as json_file:
    json_content = json_file.read()

# Extract individual JSON objects using regular expression
pattern = re.compile(r'{[^{}]*"DeletionURL"[^{}]*}')
matches = pattern.findall(json_content)

# Initialize the Selenium web driver
driver = webdriver.Chrome()  # Make sure to have Chrome driver installed

# Process each extracted JSON object
for match in matches:
    try:
        entry = json.loads(match)
        deletion_url = entry.get("DeletionURL")

        if deletion_url:
            print("Found DeletionURL:", deletion_url)

            # Open the deletion link in a web browser
            driver.get(deletion_url)

            # Find and click the "Yes" button
            try:
                yes_button = driver.find_element(By.CSS_SELECTOR, ".delete.button.right button")
                yes_button.click()
            except NoSuchElementException:
                print("Failed to locate the 'Yes' button.")
            except TimeoutException:
                print("Timeout while waiting for the 'Yes' button to appear.")

            # Optional: Wait for a short time before opening the next link
            time.sleep(2)

            # Unsure on imgur's limit
            if count == 100:
                break

            # Remove the processed entry from the JSON content
            json_content = json_content.replace(match, "")

        count = count + 1

    except json.JSONDecodeError:
        print("Failed to parse JSON:", match)
else:
    print("No entries with DeletionURL found.")

# Close the web driver
driver.quit()

# Write the modified JSON content back to the file
with open(history_file_path, "w", encoding="utf-8") as json_file:
    json_file.write(json_content)
