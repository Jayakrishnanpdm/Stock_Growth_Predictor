import os
import requests
import pickle
import pandas as pd
import numpy as np
from decouple import config
from utils.types import StockSymbols
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class StockTrainModel:

    def tune_dataset(self):
        self.dataset['timestamp'] = pd.to_datetime(self.dataset.timestamp)
        self.dataset.sort_values(by='timestamp', inplace=True)

    def train_dataset(self, folderpath: str):
        split_data = self.dataset['timestamp'].iloc[-100]  
        train_data = self.dataset[self.dataset['timestamp'] < split_data]
        X_train = train_data[['open', 'high', 'low', 'volume']]
        y_train = train_data['close']
        self.model = LinearRegression()
        self.model.fit(X_train,y_train)
        with open(f"{folderpath}/_model.pkl", 'wb') as file:
            pickle.dump(self.model, file)

    def all_operations(self, folderpath: str):
        self.dataset=pd.read_csv(f"{folderpath}/data.csv")
        self.tune_dataset()
        self.train_dataset(folderpath)

def predict_stock(company):
    API_KEY = config("API_KEY")
    if not company in StockSymbols.__members__:
        raise ValueError("Company not found in enum")
    company_code = StockSymbols[company].value
    folderpath = f"data/{company}"
    URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={company_code}&interval=60min&apikey={API_KEY}"
    response = requests.get(URL)
    try:
        data = list(response.json()['Time Series (60min)'].values())[0]
    except KeyError:
        raise ValueError("API Error")
    with open(f"{folderpath}/_model.pkl", 'rb') as file:
        model = pickle.load(file)
    X_test = np.array([data['1. open'], data['2. high'], data['3. low'], data['5. volume']]).reshape(1, -1)
    return model.predict(X_test)[0], data


def get_actual_and_predicted_data(model):
    if not model in StockSymbols.__members__:
        raise ValueError("Company not found in enum")
    folderpath = f"data/{model}"
    dataset=pd.read_csv(f"{folderpath}/data.csv")
    dataset['timestamp'] = pd.to_datetime(dataset.timestamp)
    dataset.sort_values(by='timestamp', inplace=True)
    split_data = dataset['timestamp'].iloc[-20]  
    predict_data = dataset[dataset['timestamp'] >= split_data]
    with open(f"{folderpath}/_model.pkl", 'rb') as file:
        model = pickle.load(file)
    X_test = predict_data[['open', 'high', 'low', 'volume']]
    y_test = np.array([predict_data['close']])
    y_pred = np.array([model.predict(X_test)])
    return metrics.mean_squared_error(y_test, y_pred), { 'Actual': y_test[0], 'Predicted': y_pred[0]}