"""
Copyright (c) hakuei(https://github.com/hakuei0115)

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""
"""
這個程式是用來爬取並自動提交稅務網站上的表單
主要目的是處理驗證碼,確保表單的正確提交
這個腳本使用Selenium和Tesseract OCR來實現自動化流程 https://digi.bib.uni-mannheim.de/tesseract/
在執行之前,請確保已經安裝必要的庫,如selenium、pytesseract等
"""

import os
import re
import time
import string
import requests
import pytesseract
from PIL import Image, ImageOps, ImageFilter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException


def custom_ocr(image):
    # 使用 pytesseract 辨識文字
    text = pytesseract.image_to_string(image, lang='eng')
    
    cleaned_text = text.replace(" ", "").replace("\n", "").replace("\r", "")

    return cleaned_text


def preprocess_captcha(captcha_path):
    # 讀取圖片
    image = Image.open(captcha_path)
    
    # 轉換為灰度圖片
    gray_image = ImageOps.grayscale(image)
    
    # 進行二值化處理
    threshold = 150
    binary_image = gray_image.point(lambda p: p > threshold and 255)

    # 使用不同的濾波器平滑圖像
    smoothed_image = binary_image.filter(ImageFilter.GaussianBlur(radius=1))
    
    # 去除干擾線
    cleaned_image = smoothed_image.filter(ImageFilter.MedianFilter)
    
    return cleaned_image


def download_and_preprocess_captcha(driver):
    img_element = driver.find_element(By.CSS_SELECTOR, 'img.mr-2')
    img_url = img_element.get_attribute("src")
    response = requests.get(img_url)

    with open(f'tmp_image.jpg', "wb") as img_file:
        img_file.write(response.content)

    captcha_image = preprocess_captcha('tmp_image.jpg')
    return captcha_image


def scrape_and_submit():
    # 初始化 WebDriver
    driver = webdriver.Chrome()
    number = "70747419"

    try:
        # 打開網頁
        url = "https://www.etax.nat.gov.tw/etwmain/etw113w1/ban/query"
        driver.get(url)
        time.sleep(2)

        # 輸入發票號碼範圍
        input1 = driver.find_element("id", "ban")
        input1.send_keys(number)

        # 下載並處理驗證碼圖片
        image = download_and_preprocess_captcha(driver)
    
        # 辨識文字
        result = custom_ocr(image)

        # 如果辨識結果不符合預期，重新處理驗證碼
        while True:
            print(f"Result: {result}, Length: {len(result)}")
            button_refresh = driver.find_element(By.CSS_SELECTOR, ".btn.btn-outline-brown-light.etw-icon.etw-refresh.mr-2")
            button_refresh.click()
            time.sleep(2)
            image = download_and_preprocess_captcha(driver)
            result = custom_ocr(image)
            if result == "" or result is None or len(result) != 6 or re.fullmatch("^[a-zA-Z0-9]+$", result) is None:
                # 任一條件滿足就繼續迴圈
                print("Continue loop")
                continue
            else:
                # 所有條件都不滿足，跳出迴圈
                print("Break loop")
                break

        # 輸入辨識結果
        input3 = driver.find_element("id", "captchaText")
        input3.send_keys(result)

        # 提交表單
        button_element = driver.find_element("css selector", "button[type='submit']")
        button_element.click()

        time.sleep(1)

        try:
            div_check = driver.find_element(By.ID, "dialog-desc")
            if div_check:
                while True:
                    try:
                        print('驗證中.....')
                        # 驗證碼錯誤，重新處理
                        time.sleep(2)
                        button_check = driver.find_element(By.CSS_SELECTOR, ".btn.btn-outline-dark")
                        button_check.click()
                        time.sleep(2)
                        image = download_and_preprocess_captcha(driver)
                        result = custom_ocr(image)
                        input3.clear()
                        input3.send_keys(result)
                        button_element.click()
                    except (NoSuchElementException, StaleElementReferenceException):
                        # 如果找不到元素或發生 StaleElementReferenceException，則跳出迴圈
                        print("找不到訊息 div，或元素不在 DOM 中")
                        break
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(3)
        print('你在這')
        person_company = driver.find_elements(By.CSS_SELECTOR, ".col-6.text-right.text-md-left")
        person_serial_number = person_company[0].text
        person_business_status = driver.find_element(By.CSS_SELECTOR, ".col-6.text-right.text-md-left.text-red-dark").text
        company_name = person_company[3].text
        company_type = person_company[6].text

        # 檢查是否有發票
        button_check_bill = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-brown-light.ml-0.ml-md-2.mr-2")))
        button_check_bill.click()
        p_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'text-justify.text-red-dark.mb-0'))
        )
        p_text = p_element.text

        print(f"營業人統一編號:{person_serial_number}, 營業狀況:{person_business_status}, 營業人名稱:{company_name}, 組織種類:{company_type}, {p_text}")
    finally:
        try:
            # 等待瀏覽器完全關閉
            WebDriverWait(driver, 10).until(lambda x: x.service.process is None)
        except TimeoutException:
            print("等待瀏覽器關閉超時")

        # 刪除暫存圖片
        os.remove('tmp_image.jpg')


if __name__ == '__main__':
    scrape_and_submit()