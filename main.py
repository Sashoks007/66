import numpy as np
from pymongo import MongoClient
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from datetime import datetime, timedelta

def get_forecast_parameters():
    start_date_str = input("Введите дату начала прогноза (например, 2023-01-01 00:00): ")
    forecast_hours = int(input("Сколько часов предсказать после этой даты? "))
    return start_date_str, forecast_hours

def load_data_for_prediction(start_date_str, forecast_hours):
    client = MongoClient('localhost', 27017)
    db = client.housing_data
    collection = db.california_housing

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
    end_date = start_date + timedelta(hours=forecast_hours)

    cursor = collection.find({'date': {'$gte': start_date, '$lt': end_date}})
    df = pd.DataFrame(list(cursor))

    return df

def predict_xgboost(df):
    if df.empty:
        print("Нет доступных данных для указанной даты.")
        return

    features = df[['feature1', 'feature2', 'feature3', 'feature4', 'feature5']].values  # Замените названия столбцов на реальные признаки из нового датасета
    scaler = MinMaxScaler(feature_range=(0, 1))
    features_scaled = scaler.fit_transform(features)

    model = xgb.XGBRegressor()
    model.load_model('mymodel_mongo/my_xgb_model.json')

    predictions = model.predict(features_scaled)
    return predictions

def save_predictions_to_mongo(start_date_str, predictions):
    client = MongoClient('localhost', 27017)
    db = client.housing_data
    collection = db.prediction_gboost

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
    for i, pred in enumerate(predictions):
        timestamp = start_date + timedelta(hours=i)
        prediction_document = {
            "timestamp": timestamp,
            "PM2.5": float(pred)
        }
        collection.update_one({"timestamp": timestamp}, {"$set": prediction_document}, upsert=True)

def print_and_save_predictions(start_date_str, predictions):
    print("Прогнозируемый уровень PM2.5:")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
    for i, pred in enumerate(predictions):
        timestamp = (start_date + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M')
        print(f"- Дата и время: {timestamp}, PM2.5: {pred:.2f} мкг/м³")
    save_predictions_to_mongo(start_date_str, predictions)

def main():
    start_date_str, forecast_hours = get_forecast_parameters()
    df = load_data_for_prediction(start_date_str, forecast_hours)
    predictions = predict_xgboost(df)
    if predictions is not None:
        print_and_save_predictions(start_date_str, predictions)

if __name__ == '__main__':
    main()