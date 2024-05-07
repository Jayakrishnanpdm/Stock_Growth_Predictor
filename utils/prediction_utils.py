import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class StockPredictor:

    def tune_dataset(self):
        self.dataset['Date'] = pd.to_datetime(self.dataset.Date)
        self.dataset.drop('Adj Close',axis = 1, inplace = True)
        self.dataset.sort_values(by='Date', inplace=True)

    def train_dataset(self):
        split_date = self.dataset['Date'].iloc[-1]  # Latest date
        train_data = self.dataset[self.dataset['Date'] < split_date]
        X_train = train_data[['Open', 'High', 'Low', 'Volume']]
        y_train = train_data['Close']
        self.model = LinearRegression()
        self.model.fit(X_train,y_train)  

        split_date = self.dataset['Date'].iloc[-1]  # Latest date
        self.predict = self.dataset[self.dataset['Date'] > split_date][['Open', 'High', 'Low', 'Volume']] 

    def predict_data(self):
        return self.model.predict(self.predict)

    def all_operations(self, filename: str):
        self.dataset=pd.read_csv(filename)
        self.tune_dataset()
        self.train_dataset()
        return self.predict_data()
