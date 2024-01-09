# 載入必要的套件
import pandas as pd
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import DenseNet201
from keras import layers, models

# 設定圖像資料生成器
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)  # 將像素值縮放到0~1之間，並分割出20%的資料作為驗證集
num_classes = 20


# 設定訓練集和驗證集的資料生成器
train_generator = datagen.flow_from_dataframe(
    dataframe=pd.read_csv('train_data/train_label.csv'),
    directory='train_data',  # 請替換為你的圖片資料夾路徑
    x_col='image_filename',  # 請替換為你的CSV中圖片檔案名稱的欄位
    y_col='label',  # 請替換為你的CSV中標籤的欄位
    subset='training',
    batch_size=32,
    seed=42,
    shuffle=True,
    class_mode='categorical',
    target_size=(224, 224)
)

valid_generator = datagen.flow_from_dataframe(
    dataframe=pd.read_csv('validation_data/validation.csv'),
    directory='validation_data',
    x_col='image_filename',
    y_col='label',
    subset='validation',
    batch_size=32,
    seed=42,
    shuffle=True,
    class_mode='categorical',
    target_size=(224, 224)
)

# 建立DenseNet201模型
base_model = DenseNet201(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')  # num_classes 是你的分類數量
])

# 編譯模型
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 訓練模型
model.fit(train_generator, epochs=10, validation_data=valid_generator)

# 保存模型
model.save('image_recognition_model_V1.h5')