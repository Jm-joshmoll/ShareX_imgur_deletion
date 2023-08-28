"""
Script to Open and Delete Files Using Selenium

This script reads entries from a JSON file named 'History.json' with unconventional format,
transforms the content into valid JSON format, extracts the 'DeletionURL' from each entry,
opens the URL using Selenium WebDriver, and clicks the 'Yes' button to confirm the deletion.

Make sure to install the required dependencies before running the script:
- Selenium: pip install selenium

Note:
- This script assumes you have a WebDriver (e.g., ChromeDriver) properly installed and configured.
- Be cautious when automating deletion actions as they cannot be undone.

Usage:
1. Fill in the 'history_file_path' variable with the path to your 'History.json' file.
2. Run the script using: python script.py
"""

import ast
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Path to ShareX's History.json file
history_file_path = "path/to/ShareX/History.json"  # Replace with the correct path

# Initialize the Selenium web driver
driver = webdriver.Chrome()  # Make sure to have Chrome driver installed

# Read and preprocess each line from the file
preprocessed_lines = []

with open(history_file_path, "r", encoding="utf-8") as json_file:
    for line in json_file:
        line = line.strip()
        if line.startswith('"DeletionURL"'):
            preprocessed_lines.append(line)

# Process each entry in the preprocessed lines
for line in preprocessed_lines:
    try:
        entry = ast.literal_eval("{" + line + "}")
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

            # Wait for a short time before opening the next link
            time.sleep(5)

    except (ValueError, SyntaxError):
        print("Failed to parse line:", line)  # Ignore lines that aren't valid literal objects

# Close the web driver
driver.quit()

print(f"Deletion process completed.")
