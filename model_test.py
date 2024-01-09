import tensorflow as tf
from keras.preprocessing import image
from keras.applications.densenet import preprocess_input
import numpy as np
import pandas as pd

# 載入訓練好的模型
model = tf.keras.models.load_model('image_recognition_model.h5')  # 替換成實際模型的路徑

# 載入測試圖片
img_path = 'image1.jpg'  # 替換成實際測試圖片的路徑
img = image.load_img(img_path, target_size=(224, 224))

# 將圖片轉換成模型可接受的格式
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

# 辨識圖片
predictions = model.predict(img_array)

# 載入CSV檔案
csv_path = 'train_data/train_label.csv'  # 替換成實際CSV檔案的路徑
df = pd.read_csv(csv_path)

# 找到最大概率對應的類別索引
predicted_class_index = np.argmax(predictions)

# 根據索引找到對應的類別標籤
predicted_class_label = df['label'].iloc[predicted_class_index]

# 顯示預測結果
print(f"Predicted class: {predicted_class_label}")
