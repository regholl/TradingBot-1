import threading
import configparser
from abc import ABC, abstractmethod
import ccxt
import pandas as pd
import numpy as np


class TechnicalIndicators(): 
    def __init__(self):
        pass

    # Define function to calculate moving average
    def moving_average(self, data, window):
        '''Calculate the moving average of a given dataset.
        
        Args:
            data (pandas.Series): The dataset to calculate the moving average for.
            window (int): The size of the window to use for the moving average calculation.
        
        Returns:
            pandas.Series: The moving average of the given dataset.
        '''
        weights = np.repeat(1.0, window)/window
        smas = np.convolve(data, weights, 'valid')
        return smas

    # Define function to calculate relative strength index (RSI)
    def relative_strength_index(self, data, window):
        '''Calculate the relative strength index (RSI) of a given dataset.
        
        Args:
            data (pandas.Series): The dataset to calculate the RSI for.
            window (int): The size of the window to use for the RSI calculation.
        
        Returns:
            pandas.Series: The RSI of the given dataset.
        '''
        delta = data.diff()
        delta = delta[1:]
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        roll_up = up.rolling(window).mean()
        roll_down = down.abs().rolling(window).mean()
        rs = roll_up / roll_down
        rsi = 100.0 - (100.0 / (1.0 + rs))
        return rsi

    # Define function to calculate stochastic oscillator
    def stochastic_oscillator(self, high, low, close, n):
        '''Calculate the stochastic oscillator of a given dataset.
        
        Args:
            high (pandas.Series): The high values of the dataset.
            low (pandas.Series): The low values of the dataset.
            close (pandas.Series): The close values of the dataset.
            n (int): The size of the window to use for the stochastic oscillator calculation.
        
        Returns:
            pandas.Series: The stochastic oscillator of the given dataset.
        '''
        lowest_low = low.rolling(window=n).min()
        highest_high = high.rolling(window=n).max()
        k = 100 * (close - lowest_low)/(highest_high - lowest_low)
        return k
    
    # Calculate the moving average convergence divergence of a given data series
    def macd(self, data):
        ema_12 = data.ewm(span=12, adjust=False).mean()
        ema_26 = data.ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal

# Abstract Parent class
class TradingSystem(ABC):
    def __init__(self, api, symbol, time_frame, system_id, system_label):
        tech_indicators = TechnicalIndicators()
        api_key = 'YOUR_API_KEY'
        api_secret = 'YOUR_API_SECRET'

        # Initialize Binance client
        binance = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret
        })
        self.api = api
        self.symbol = symbol
        self.time_frame = time_frame
        self.system_id = system_id
        self.system_label = system_label
        thread = threading.Thread(target=self.system_loop)
        thread.start()

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

class Binance(TradingSystem):

    def analyze_asset(self):
        # Implement analyze_asset logic here
        pass

    # Function to perform market buy
    def market_buy(symbol, amount):
        order = binance.create_market_buy_order(symbol, amount)
        return order

    # Function to perform market sell
    def market_sell(symbol, amount):
        order = binance.create_market_sell_order(symbol, amount)
        return order

    # Function to perform limit buy
    def limit_buy(symbol, amount, price):
        order = binance.create_limit_buy_order(symbol, amount, price)
        return order

    # Function to perform limit sell
    def limit_sell(symbol, amount, price):
        order = binance.create_limit_sell_order(symbol, amount, price)
        return order

    def system_loop(self):
        # Implement system_loop logic here
        pass