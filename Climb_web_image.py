import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument('--headless')

# select1_element = driver.find_element("id", "invoiceMonth")
# select1 = Select(select1_element)
# select1.select_by_visible_text("112年07月~08月")

for i in range(301, 401):
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://www.etax.nat.gov.tw/etwmain/etw113w2"
    driver.get(url)

    time.sleep(2)

    img_element = driver.find_element(By.CSS_SELECTOR, 'img.mr-2')
    img_url = img_element.get_attribute("src")
    response = requests.get(img_url)
    with open(f'train_data/image{i}.jpg', "wb") as img_file:
        img_file.write(response.content)
    
    time.sleep(3)
    driver.quit()


# img_element.screenshot('captcha.png')
print("Done!")


