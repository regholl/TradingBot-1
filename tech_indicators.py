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


    # Moving Average Crossover (MAC) trading strategy 
    def mac_strategy(self, data):
        short_window = 50
        long_window = 200

        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

        signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
        signals['positions'] = signals['signal'].diff()

        if signals['positions'].iloc[-1] == 1.0:
            mac_signal = "BUY"
        elif signals['positions'].iloc[-1] == -1.0:
            mac_signal = "SELL"
        else:
            mac_signal = "HOLD"
            
        return mac_signal
    
    # Function to plot.
    def plot_data(self, data):
        data = data[-90:]
        data['12-SMA'] = data.Close.rolling(window=12).mean()
        data['26-SMA'] = data.Close.rolling(window=26).mean()
        mpf.plot(data,type='line',mav=(12,26),figsize=(15,7), title='Technical Analysis',
                ylabel='Price (USD)')