import threading
import configparser
from abc import ABC, abstractmethod
import ccxt
import pandas as pd
import numpy as np
import configparser
import tech_indicators as TechInd
import logging
import fetch_data as fetchData

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "logs/logfile.log", filemode = "w", format = Log_Format,level = logging.DEBUG)
logger = logging.getLogger()

# Abstract Parent class
class TradingSystem(ABC):
    def __init__(self, api, symbol, time_frame, system_id, system_label):
        data_fetcher = fetchData()
        tech_indicators = TechInd()
        self.config = self.read_config()

        # Initialize Binance client
        self.binance = ccxt.binance({
            'apiKey': self.config.get("Binance", "api_key"),
            'secret': self.config.get("Binance", "api_secret"),
        })

        self.api = api
        self.symbol = symbol
        self.time_frame = time_frame
        self.system_id = system_id
        self.system_label = system_label
        thread = threading.Thread(target=self.system_loop)
        thread.start()

    def read_config(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config
    
    @abstractmethod
    def analyze_asset(self):
        pass

    @abstractmethod
    def market_buy(self):
        pass

    @abstractmethod
    def market_sell(self):
        pass
    
    @abstractmethod
    def limit_buy(self):
        pass
    
    @abstractmethod
    def limit_sell(self): 
        pass

    @abstractmethod
    def system_loop(self):
        pass


class AlpacaSystem(TradingSystem):

    def __init__(self, api, symbol, time_frame, system_id, system_label):
        super().__init__(api, symbol, time_frame, system_id, system_label)
        self.data_fetcher = fetch_data.FetchData()
        self.tech_indicators = tech_indicators.TechIndicators()

    def analyze_asset(self):
        # Implement analyze_asset logic here
        pass

    def market_buy(self, qty):
        order = self.api.submit_order(
            symbol=self.symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        return order

    def market_sell(self, qty):
        order = self.api.submit_order(
            symbol=self.symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        return order

    def limit_buy(self, qty, price):
        order = self.api.submit_order(
            symbol=self.symbol,
            qty=qty,
            side='buy',
            type='limit',
            time_in_force='gtc',
            limit_price=price
        )
        return order

    def limit_sell(self, qty, price):
        order = self.api.submit_order(
            symbol=self.symbol,
            qty=qty,
            side='sell',
            type='limit',
            time_in_force='gtc',
            limit_price=price
        )
        return order

    def system_loop(self):
        # Implement system_loop logic here
        pass

class BinanceSystem(TradingSystem):
    def __init__(self, api, symbol, time_frame, system_id, system_label):
        super().__init__(api, symbol, time_frame, system_id, system_label)
        self.data_fetcher = fetch_data.FetchData()
        self.tech_indicators = tech_indicators.TechIndicators()

    def analyze_asset(self):
        # Implement analyze_asset logic here
        pass

    # Function to perform market buy
    def market_buy(symbol, amount):
        order = self.binance.create_market_buy_order(symbol, amount)
        return order

    # Function to perform market sell
    def market_sell(symbol, amount):
        order = self.binance.create_market_sell_order(symbol, amount)
        return order

    # Function to perform limit buy
    def limit_buy(symbol, amount, price):
        order = self.binance.create_limit_buy_order(symbol, amount, price)
        return order

    # Function to perform limit sell
    def limit_sell(symbol, amount, price):
        order = self.binance.create_limit_sell_order(symbol, amount, price)
        return order

    def system_loop(self):
        # Implement system_loop logic here
        pass