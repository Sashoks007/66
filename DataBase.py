import numpy as np
import os
from pymongo import MongoClient
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb


def load_and_prepare_data_mongo():
    client = MongoClient('localhost', 27017)
    db = client.housing_data
    collection = db.california_housing

    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))

    features = df[['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms']].values  # Замените названия столбцов на реальные признаки из нового датасета
    target = df['median_house_value'].values

    scaler = MinMaxScaler(feature_range=(0, 1))
    features_scaled = scaler.fit_transform(features)

    return features_scaled, target


def train_xgboost():
    X, y = load_and_prepare_data_mongo()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.08, gamma=0, subsample=0.75, colsample_bytree=1,
                             max_depth=7)
    model.fit(X_train, y_train)

    model_dir = 'mymodel_mongo'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model.save_model(f'{model_dir}/my_xgb_model.json')

    print("Модель успешно обучена и сохранена.")


if __name__ == '__main__':
    train_xgboost()