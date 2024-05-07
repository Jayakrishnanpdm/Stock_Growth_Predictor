from enum import Enum


class StockSymbols(Enum):
    META = "Meta"
    APPLE = "AAPL"
    MICROSOFT = "MSFT"
    AMAZON = "AMZN"
    ALPHABET = "GOOGL"
    IBM = "IBM"
    TESLA = "TSLA"

    def get_all_symbols():
        return {symbol.name: symbol.value for symbol in StockSymbols}
