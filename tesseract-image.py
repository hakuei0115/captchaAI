import os
import pytesseract
import tempfile
import csv
from PIL import Image, ImageOps, ImageFilter

with open('test.csv', 'w', newline='\n', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['image_filename', 'label'])

def preprocess_captcha(captcha_path):
    # 讀取圖片
    image = Image.open(captcha_path)
    
    # 轉換為灰度圖片
    gray_image = ImageOps.grayscale(image)
    
    # 進行二值化處理
    threshold = 150  # 你可以調整這個閾值來適應不同的驗證碼
    binary_image = gray_image.point(lambda p: p > threshold and 255)

    # 使用不同的濾波器平滑圖像
    smoothed_image = binary_image.filter(ImageFilter.GaussianBlur(radius=1))
    
    # 去除干擾線
    cleaned_image = smoothed_image.filter(ImageFilter.MedianFilter)
    
    return cleaned_image

def custom_ocr(image):
    # 使用 pytesseract 辨識文字，設定 config 參數
    text = pytesseract.image_to_string(image, lang='eng')
    
    cleaned_text = text.replace(" ", "").replace("\n", "").replace("\r", "")
    
    return cleaned_text

for i in range(200, 301):
    captcha_path = f"train_data/image{i}.jpg"
    processed_image = preprocess_captcha(captcha_path)    
    # processed_image.save(f"trash/processed_image{i}.jpg")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_filename = temp_file.name
        processed_image.save(temp_filename)

        # 假設這裡是你的 custom_ocr 函式的呼叫
        result = custom_ocr(Image.open(temp_filename))

    # image = Image.open(f"trash/processed_image{i}.jpg")
    # result = custom_ocr(image)

    with open('test.csv', 'a', newline='\n', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([f"image{i}.jpg", result])
    # 刪除臨時檔案
    os.remove(temp_filename)

# 使用例子
# captcha_path = "image20.jpg"
# processed_image = preprocess_captcha(captcha_path)

# # 顯示處理後的圖片
# processed_image.show()
# processed_image.save("captcha.jpg")
# image = Image.open("captcha.jpg")
# text = pytesseract.image_to_string(image, lang='eng')
# cleaned_text = text.replace("\n", "").replace("\r", "").replace(" ", "")
# print(cleaned_text)

print("Done!")  