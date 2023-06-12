#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pytesseract
from base64 import b64decode
import re

url = "http://34.124.157.94:5003/"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

with webdriver.Chrome(ChromeDriverManager().install(), options=options) as driver:
    driver.get(url)
    score = 0
    while score < 100:
        img_captcha = driver.find_element(By.CLASS_NAME, 'img-fluid')
        score = int(driver.find_element(By.TAG_NAME, 'h3').text.split()[-1])
        print(score)
        img_base64 = img_captcha.get_attribute("src").split(',')[-1]
        with open('./captcha.jpeg', 'wb') as f:
            f.write(b64decode(img_base64))
        captcha = pytesseract.image_to_string(
            "./captcha.jpeg")  # , config="--psm 10")
        input_box = driver.find_element(By.ID, 'captch_form')
        input_box.send_keys(captcha + Keys.RETURN)

    page = driver.page_source
    print(re.findall(r"grey\{.+\}", page))
