# Import necessary libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
import yfinance as yf


class dataggregator(): 

    
    def __init__(self): 
        pass

    def fetchCryptoNews(self):
        # Fetch Crypto News
        # Define search terms
        search_terms = "current cryptocurrency market trends"

        # Fetch search results
        url = f"https://www.google.com/search?q={search_terms}&tbm=nws"
        res = requests.get(url)
        res.raise_for_status()

        # Parse search results
        soup = BeautifulSoup(res.text, "html.parser")
        search_results = soup.select(".dbsr")
        top_ten_results = [result.a.text for result in search_results[:10]]

        # Print top 10 results
        for i in range(len(top_ten_results)):
            print(f"{i+1}. {top_ten_results[i]}")


    def extract_financial_news(self):
        # Define the URL to extract news from
        url = 'https://www.marketwatch.com/newsviewer'

        # Send an HTTP request to the URL
        response = requests.get(url)

        # Extract the HTML content
        content = response.content

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Extract the news articles from the parsed content
        articles = soup.find_all('div', {'class': 'article__content'})

        # Filter out non-financial news articles
        filtered_articles = []

        for article in articles:
            if 'marketwatch.com/story/' in article.find('a')['href']:
                filtered_articles.append(article)

        return filtered_articles

    # Fetch Asset Prices 
    def fetchAssetPrices(self, symbol_list, dir_path): 
        # # specify the list of cryptocurrencies and stocks you want to download
        # symbol_list = ['BTC', 'ETH', 'AMZN', 'AAPL', 'FB', 'GOOG', 'MSFT', 'NFLX', 'TSLA']

        # # define the directory to save the downloaded data
        # dir_path = './data/'

        # create the directory if it does not exist
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # define the range of dates to download weekly data
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=365)
        delta = timedelta(weeks=1)

        # function to download data from cryptocompare
        def download_cryptocompare_data(symbol):
            url = 'https://min-api.cryptocompare.com/data/histoday'
            params = {'fsym': symbol, 'tsym': 'USD', 'limit': '2000'}

            # download data from cryptocompare
            response = requests.get(url, params=params)
            data = response.json()['Data']

            # create a pandas dataframe from the downloaded data
            df = pd.DataFrame(data)
            df['time'] = pd.to_datetime(df['time'], unit='s').dt.date

            # filter the data based on the specified date range
            mask = (df['time'] >= start_date) & (df['time'] <= end_date)
            df = df.loc[mask]

            # save the data to a CSV file
            file_path = os.path.join(dir_path, f'{symbol}_cryptocompare.csv')
            df.to_csv(file_path, index=False)

        # function to download data from yahoo finance
        def download_yahoo_finance_data(symbol):
            url = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}'
            params = {'interval': '1wk', 'range': '1y', 'events': 'history', 'includeAdjustedClose': 'true'}

            # download data from yahoo finance
            response = requests.get(url, params=params)
            data = response.content.decode().split('\n')
            headers = data[0].split(',')
            headers[0] = 'date'

            # create a pandas dataframe from the downloaded data
            df = pd.DataFrame(columns=headers)
            for row in data[1:-1]:
                row_data = row.split(',')
                row_data[0] = datetime.strptime(row_data[0], "%Y-%m-%d").date()
                df = df.append(pd.Series(row_data, index=headers), ignore_index=True)

            # filter the data based on the specified date range
            mask = (df['date'] >= start_date) & (df['date'] <= end_date)
            df = df.loc[mask]

            # save the data to a CSV file
            file_path = os.path.join(dir_path, f'{symbol}_yahoo_finance.csv')
            df.to_csv(file_path, index=False)

        # loop through the list of symbols and download the data
        for symbol in symbol_list:
            print(f'Downloading data for {symbol}')
            download_cryptocompare_data(symbol)
            download_yahoo_finance_data(symbol)
            print('Data download completed successfully!')
    
    def fetchYfinanceAPI(self,symbol, start_date, end_date):

        # Fetch data from yahoo finance API for Cryptocurrency
        crypto_data = yf.download(symbol, start=start_date, end=end_date)

        # View the data
        print(crypto_data)