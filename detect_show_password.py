import time
import json
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

# Initiate webdriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open url
url = "https://login.squarespace.com/"
driver.get(url)

# Parse url to get domain name
parsed_url = urlsplit(url)
domain = parsed_url.netloc.split('.')[-2]

# Take screenshot
driver.set_window_size(800, 600)
driver.save_screenshot(f"{domain}.png")


global xpath

# Get page source
page_source = driver.page_source

# Parse page source
soup = BeautifulSoup(page_source, 'html.parser')

# Find all elements
elements = soup.find_all(True)

# Attribute values to look for
attr_values = ['show password', 'Show password', 'show-password', 'Show-password', 'show_password', 'Show_password','Show','show','Hide','hide','Reveal','reveal']

# Finds matching attribute values and generates xpath
for element in elements:
    for attr, value in element.attrs.items():
        if value in attr_values:
            xpath = f"//{element.name}[@{attr}='{value}']"
            print(xpath)
        else:
            print(f'No matching attribute values found')
try:
    driver.find_element(By.XPATH, xpath)
    print('element found')
except NoSuchElementException:
    print("No such element")


# Create json file
data = [
    {
        "url": f"{url}",
        "png_path":f"{domain}.png",
        "xpath": f"{xpath}"
    }
    ]

# Write json file
for entry in data:
    json_file_path = f"{domain}.json"
    with open(json_file_path, 'w') as json_file:
        json.dump(entry, json_file, indent=4)

driver.quit()


