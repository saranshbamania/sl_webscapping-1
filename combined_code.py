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

options = Options()
options.add_argument("--start-maximized")  # Start the window maximized
options.add_argument("--disable-extensions")  # Disable extensions
options.add_argument("--disable-popup-blocking")  # Disable pop-up blocking

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://matrix.itasoftware.com/search")

try:
    # Wait for the tab elements to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'mdc-tab__text-label'))
    )
    
    # Click the second tab (if that's required for your operation)
    search_elements = driver.find_elements(By.CLASS_NAME, 'mdc-tab__text-label')
    if len(search_elements) > 1:
        search_elements[1].click()
    else:
        print("There are not enough elements with the class name to click the second one.")

    # first airport
    airport_to_search_first = "DEL"  # Replace with the first airport name you want to search for
    airport_inputs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[@placeholder='Add airport']"))
    )
    airport_input_first = airport_inputs[0]
    airport_input_first.send_keys(airport_to_search_first)
    airport_input_first.send_keys(Keys.ENTER)
    
    
    # second airport
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Add airport'])[2]"))
    )
    
    # Type in the second input box
    airport_to_search_second = "BLR"  # Replace with the second airport name you want to search for
    airport_inputs[1].clear()  # Clear any pre-filled content in the second input
    airport_inputs[1].send_keys(airport_to_search_second)
    airport_inputs[1].send_keys(Keys.ENTER)
    
    #date input
    date_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'mat-input-12'))  # ID from your provided HTML
    )
    date_input.click()  # Open the date picker

    # Now that the date picker is open, send the date to the input
    date_to_input = "10/20/2024"  # Replace with the date you want to enter
    date_input.send_keys(date_to_input)
    date_input.send_keys(Keys.ENTER)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    search_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Search')]"))
    )
    search_button.click()
    time.sleep(60)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    driver.save_screenshot("screenshot.png")
    img = cv2.imread('screenshot.png')
    x, y, width, height = 0, 450, 1267, 308  # Replace with your desired coordinates and dimensions
    cropped_img = img[y:y+height, x:x+width]
    cv2.imwrite('screenshot.png', cropped_img)
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    img = Image.open("screenshot.png")

    text = pytesseract.image_to_string(img)
    print(text)
    
    
finally:
    # Keep the browser open for inspection
    #time.sleep(10)
    #driver.quit()  # Uncomment this line if you want to close the browser at the end
    pass
