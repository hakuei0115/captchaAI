"""
Copyright (c) hakuei(https://github.com/hakuei0115)

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""
import os
import re
import time
import flask
import logging
import requests
import pytesseract
from PIL import Image, ImageOps, ImageFilter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logging.basicConfig(filename='crawler.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
app = flask.Flask(__name__)

def custom_ocr(image):
    custom_config = r'--oem 1'  # 使用 OCR 引擎模式 1 (LSTM)
    # 使用 pytesseract 辨識文字
    text = pytesseract.image_to_string(image, lang='eng', config=custom_config)
    
    cleaned_text = text.strip().replace(" ", "").replace("\n", "").replace("\r", "")

    return cleaned_text

def preprocess_captcha(captcha_path):
    # 讀取圖片
    image = Image.open(captcha_path)
    
    # 轉換為灰度圖片
    gray_image = ImageOps.grayscale(image)
    
    # 進行二值化處理
    threshold = 150
    binary_image = gray_image.point(lambda p: p > threshold and 255)
    
    return binary_image

def download_and_preprocess_captcha(driver):
    img_element = wait_for_element(driver, By.CSS_SELECTOR, 'img.mr-2')
    img_url = img_element.get_attribute("src")
    response = requests.get(img_url)

    with open(f'tmp_image.jpg', "wb") as img_file:
        img_file.write(response.content)

    captcha_image = preprocess_captcha('tmp_image.jpg')
    return captcha_image

def wait_for_element(driver, by, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except TimeoutException as e:
        raise NoSuchElementException(logging.error(f"元素未在指定時間內找到: {by} - {value}. 詳細錯誤: {e}"))

def wait_and_click(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value))).click()
    except TimeoutException as e:
        raise NoSuchElementException(logging.error(f"元素未在指定時間內找到: {by} - {value}. 詳細錯誤: {e}"))

def is_valid_result(result):
    return len(result) == 6 and re.fullmatch("^[a-zA-Z0-9]+$", result)

def webcrawler(number):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    with webdriver.Chrome(options=chrome_options) as driver:
        try:
            url = "https://www.etax.nat.gov.tw/etwmain/etw113w1/ban/query"
            driver.get(url)

            # 輸入發票號碼範圍
            input1 = wait_for_element(driver, By.ID, "ban")
            input1.send_keys(number)

            while True:
                image = download_and_preprocess_captcha(driver)

                result = custom_ocr(image)

                while not is_valid_result(result):
                    print(f"Result: {result}, Length: {len(result)}")
                    logging.error(f"辨識結果不合法: {result}")
                    button_refresh = driver.find_element(By.CSS_SELECTOR, ".btn.btn-outline-brown-light.etw-icon.etw-refresh.mr-2")
                    button_refresh.click()
                    time.sleep(2)
                    image = download_and_preprocess_captcha(driver)
                    result = custom_ocr(image)
                
                # 輸入辨識結果
                input3 = driver.find_element("id", "captchaText")
                input3.send_keys(result)

                wait_and_click(driver, By.CSS_SELECTOR, "button[type='submit']")

                time.sleep(1)

                if driver.current_url != url:
                    break

                try:
                    print("you are waiting for button to load")
                    wait_and_click(driver, By.CSS_SELECTOR, ".btn.btn-outline-dark")
                except TimeoutException as ea:
                    logging.error(f"按鈕載入超時. 詳細錯誤: {ea}")
                    print("Timed out waiting for button to load")

            # 檢查是否有發票
            wait_and_click(driver, By.CSS_SELECTOR, ".btn.btn-brown-light.ml-0.ml-md-2.mr-2")

            bill_check = wait_for_element(driver, By.CLASS_NAME, 'text-justify.text-red-dark.mb-0').text

            person_company = driver.find_elements(By.CSS_SELECTOR, ".col-6.text-right.text-md-left")
            person_serial_number = person_company[0].text
            person_business_status = driver.find_element(By.CSS_SELECTOR, ".col-6.text-right.text-md-left.text-red-dark").text
            company_name = person_company[3].text
            company_type = person_company[6].text
            return person_serial_number, person_business_status, company_name, company_type, bill_check
            # print(f"營業人統一編號:{person_serial_number}, 營業狀況:{person_business_status}, 營業人名稱:{company_name}, 組織種類:{company_type}, {bill_check}")
        
        except Exception as e:
            logging.warning(f"發生例外: {e}")

        finally:
            os.remove('tmp_image.jpg')

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    number = flask.request.form['input_data']
    result = webcrawler(number)
    return flask.render_template('index.html', input_data=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)