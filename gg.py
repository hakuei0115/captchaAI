from PIL import Image, ImageDraw, ImageFont
import random

def get_rand_color(min_val, max_val):
    """ 產生一個隨機的顏色 """
    return (random.randint(min_val, max_val), random.randint(min_val, max_val), random.randint(min_val, max_val))

def get_captcha_with_random_font_size(width, height):
    """ 產生一個帶有6個隨機字元和隨機字體大小的驗證碼圖片 """
    # 定義字元集合
    # char_set = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    char_set = 'fghklQWmw'

    # 生成一個包含6個隨機字元的字串
    random_str = ''.join(random.choices(char_set, k=6))

    # 創建一個新的白色背景圖片
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 用隨機顏色填充背景
    draw.rectangle([(0, 0), (width, height)], fill=get_rand_color(200, 250))

    # 設置一個統一的顏色作為干擾線的顏色
    line_color = get_rand_color(160, 200)

    # 繪製帶有統一顏色的隨機干擾線
    for _ in range(155):
        start = (random.randint(0, width), random.randint(0, height))
        end = (start[0] + random.randint(0, 12), start[1] + random.randint(0, 12))
        draw.line([start, end], fill=line_color, width=1)

    # 用隨機字體大小繪製字元
    char_spacing = width // 6
    for i, char in enumerate(random_str):
        font_path = "arial.ttf"
        font_size = random.randint(20, 32)  # 隨機字體大小在15到25之間
        # font = ImageFont.load_default().font_variant(size=font_size)
        font = ImageFont.truetype(font_path, size=font_size)
        bbox = draw.textbbox((0, 0), char, font=font)
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]
        x = char_spacing * i + (char_spacing - char_width) // 2
        y = (height - char_height) // 2 - 7 #TODO: 調整這裡的數值，可以根據需要微調垂直位置
        draw.text((x, y), char, font=font, fill=get_rand_color(20, 130))

    return image, random_str

# 範例使用
captcha_image_random_font, captcha_str_random_font = get_captcha_with_random_font_size(150, 50)
print(captcha_str_random_font)
captcha_image_random_font.show()  # This will open the image in the default image viewer

# 將圖片保存為檔案
captcha_image_random_font.save("captcha_random_font_size.png")