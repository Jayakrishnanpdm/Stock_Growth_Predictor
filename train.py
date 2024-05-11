import os
import requests
from decouple import config
from utils.types import StockSymbols
from utils.prediction_utils import StockTrainModel

API_KEY = config("API_KEY")

os.makedirs("data", exist_ok=True)

for key, value in StockSymbols.get_all_symbols().items():
    folderpath = f"data/{key}"
    try:
        os.makedirs(folderpath)
        URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&datatype=csv&outputsize=full&symbol={value}&apikey={API_KEY}"
        response = requests.get(URL)
        with open(f"{folderpath}/data.csv", "wb") as file:
            file.write(response.content)
        model = StockTrainModel().all_operations(folderpath)
        print(f"Model trained for {key}")
    except Exception:
        pass