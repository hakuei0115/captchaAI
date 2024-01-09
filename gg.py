from PIL import Image, ImageDraw, ImageFont
import random

def generate_verification_code(length=4):
    # 產生隨機驗證碼
    verification_code = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))

    # 設定圖片大小和背景色
    width, height = 150, 50
    background_color = (255, 255, 255)

    # 建立一個白色背景的圖片
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 設定字體和字體大小
    font_size = 25
    font = ImageFont.truetype('arial.ttf', font_size)

    # 在圖片上繪製文字
    text_position = ((width - font_size * length) / 2, (height - font_size) / 2)
    draw.text(text_position, verification_code, font=font, fill=(0, 0, 0))

    # 產生干擾線
    for _ in range(5):
        line_color = tuple(random.randint(0, 255) for _ in range(3))
        line_start = (random.randint(0, width), random.randint(0, height))
        line_end = (random.randint(0, width), random.randint(0, height))
        draw.line([line_start, line_end], fill=line_color, width=2)

    # 儲存圖片
    image.save('verification_code.png')

if __name__ == "__main__":
    generate_verification_code()
