import os
import requests
from sklearn.linear_model import LinearRegression, LogisticRegression
from .models import StockData
from datetime import datetime

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if 'Time Series (Daily)' in data:
        time_series = data['Time Series (Daily)']

        for date_str, price_data in time_series.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()

            StockData.objects.update_or_create(
                symbol=symbol,
                date=date,
                defaults={
                    'open_price': price_data['1. open'],
                    'close_price': price_data['4. close'],
                    'high_price': price_data['2. high'],
                    'low_price': price_data['3. low'],
                    'volume': price_data['5. volume'],
                }
            )
    else:
        print('Error fetching data:', data.get('Error Message', 'Unknown error'))

from sklearn.model_selection import train_test_split

logreg = LogisticRegression(random_state=16)
linreg = LinearRegression()
