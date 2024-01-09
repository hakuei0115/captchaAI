import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import DenseNet201
from keras.optimizers import Adam
from keras import layers, models

# 讀取CSV檔案
csv_path = 'train_data/train_label.csv'  # 請替換成你的CSV檔案路徑
df = pd.read_csv(csv_path)

# 切分訓練集和測試集
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# 設定圖像資料生成器
datagen = ImageDataGenerator(rescale=1./255)

# 設定訓練資料生成器
train_generator = datagen.flow_from_dataframe(
    dataframe=train_df,
    directory='train_data',  # 請替換成你的圖片檔案所在資料夾路徑
    x_col='image_filename',
    y_col='label',
    target_size=(224, 224),  # DenseNet201的預設輸入大小
    batch_size=32,
    class_mode='categorical'  # 假設是多類別分類，可依需求修改
)

# 建立DenseNet201模型
base_model = DenseNet201(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model = models.Sequential()
model.add(base_model)
model.add(layers.GlobalAveragePooling2D())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(80, activation='softmax'))  # 請替換成你的類別數量

# 編譯模型
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# 訓練模型
model.fit(train_generator, epochs=10)  # 可以根據需要調整epochs數量

# 保存模型
model.save('image_recognition_model.h5')