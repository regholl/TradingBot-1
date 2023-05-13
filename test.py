import datetime
import predictive_models as pm
from fetch_data import DataAggregator
from tech_indicators import TechnicalIndicators
import pandas as pd

def test_data_aggregator():
    aggregator = DataAggregator()
    
    # Test fetch_crypto_news
    print("Testing fetch_crypto_news:")
    aggregator.fetch_crypto_news()
    
    # Test extract_financial_news
    # print("\nTesting extract_financial_news:")
    # articles = aggregator.extract_financial_news()
    # if articles:
    #     print(f"Found {len(articles)} articles from MarketWatch.")
    # else:
    #     print("No articles found.")
    
    print("\nTesting fetch_asset_prices:")
    # Test fetch_asset_prices
    symbols = ['BTC', 'ETH']  # Add your symbols here
    directory = "./csvs"  # Add your directory here
    aggregator.fetch_asset_prices(symbols, directory, False)
    print("Exception thrown")
    
    # Test fetch_yfinance_api
    print("\nTesting fetch_yfinance_api:")
    start_date = datetime.datetime.now() - datetime.timedelta(days=365)
    end_date = datetime.datetime.now()
    data = aggregator.fetch_yfinance_api('AAPL', start_date, end_date)
    data.to_csv('csvs/AAPL.csv')


def test_tech_indicators():
    
    # Initialize TechnicalIndicators class
    ti = TechnicalIndicators()

    # Initialize Aggregator class
    aggregator = DataAggregator()

    # Fetch historical data
    # start_date = datetime.datetime.now() - datetime.timedelta(days=365)
    # end_date = datetime.datetime.now()
    # data = aggregator.fetch_yfinance_api('AAPL', start_date, end_date)

    data = pd.read_csv('csvs/AAPL.csv')
    # Calculate moving average
    ma = ti.moving_average(data['Close'], window=50)
    print("Moving Average:")
    print(ma)

    # Calculate relative strength index (RSI)
    rsi = ti.relative_strength_index(data['Close'], window=14)
    print("RSI:")
    print(rsi)

    # Calculate stochastic oscillator
    so = ti.stochastic_oscillator(data['High'], data['Low'], data['Close'], n=14)
    print("Stochastic Oscillator:")
    print(so)

    # Calculate MACD
    macd, signal = ti.macd(data['Close'])
    print("MACD:")
    print(macd)
    print("Signal:")
    print(signal)

    # Moving Average Crossover (MAC) trading strategy
    mac_signal = ti.mac_strategy(data)
    print("MAC Strategy Signal:")
    print(mac_signal)

    # Plot data
    #ti.plot_data(data)

def test_models():
    # Use pandas to load your data.
    data = pd.read_csv('csvs/AAPL.csv')

    # Create models
    linear_regressor = pm.LinearRegressor()
    rnn = pm.RNN()
    lstm = pm.LSTMModel()
    hmm = pm.HMM()

    # Train models
    print("Training LinearRegressor...")
    linear_regressor.train(data)

    print("Training RNN...")
    rnn.train(data)

    print("Training LSTM...")
    lstm.train(data)

    print("Training HMM...")
    hmm.train(data)

    # Test models on some data
    X_test = data.drop(['Close'], axis=1).iloc[-10:]  # last 10 rows
    print("Predictions:")
    print("LinearRegressor:", linear_regressor.predict(X_test))
    print("RNN:", rnn.predict(X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))))
    print("LSTM:", lstm.predict(X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))))
    print("HMM:", hmm.predict())

    # Print HMM details
    print("HMM details:")
    hmm.print_details()

if __name__ == "__main__":
    #test_data_aggregator()
    test_tech_indicators()
    test_models()