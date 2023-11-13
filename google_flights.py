#written by saransh and prateek iit bombay
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument("--start-maximized")  # Start the window maximized
options.add_argument("--disable-extensions")  # Disable extensions
options.add_argument("--disable-popup-blocking")  # Disable pop-up blocking

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.google.com/travel/flights")

css_selector = '.rYD0Re.P2UJoe'  # This targets an element with both rYD0Re and P2UJoe classes

# Locate the element using the CSS selector
#safe_area = driver.find_element(By.CSS_SELECTOR, css_selector)

# Use ActionChains to perform the click action
#ActionChains(driver).move_to_element(safe_area).click().perform()

wait = WebDriverWait(driver, 10)
input_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[jsname="yrrlRe"]')))

# Click the input box
input_box.click()

# Clear the input box if needed
input_box.clear()

# Type your text into the input box
text_to_type = 'Your Text Here'  # Replace with the text you want to type in
input_box.send_keys(text_to_type)

# Press Enter
input_box.send_keys(Keys.RETURN)

