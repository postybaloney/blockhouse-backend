import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from .models import StockData

def get_data(symbol, days):
    """
    Fetch the stock data from the PostGreSQl for a specific symbol and for specific days
    """
    stock_data_for_specific_days = StockData.objects.filter(symbol=symbol).order_by('-date')[:days]
    df = pd.DataFrame(list(stock_data_for_specific_days.values('date', 'close_price')))
    df = df.sort_values(by='date')
    return df

def train_model(data):
    """
    Training a Linear model for the stock data
    """
    X = np.arange(len(data)).reshape(-1, 1)
    Y = data['close_price'].values

    model = LinearRegression()
    model.fit(X, Y)

    return model

def predict_prices(symbol, days=30):
    """
    Predict for the next days given specific, I am defining as 730 (365 * 2), previous days using the linear model
    """
    df = get_data(symbol=symbol, days=730) # Getting previous 2 years of data

    model = train_model(df) # Training the model

    # Predict future prices for next user-defined quantity of days
    future_X = np.arange(len(df), len(df) + days).reshape(-1, 1) # Future days as input
    predictions = model.predict(future_X) # Predictions

    for i in range(days):
        next_pred = predictions[i]
        StockData.objects.create(
            symbol=symbol,
            date = pd.Timestamp.now() + pd.Timedelta(days=i+1), # Simulate future days
            open_price = 0,
            high_price = 0,
            low_price = 0,
            volume = 0,
            close_price = next_pred,
            is_predicted=True # Tells this is a prediction
        )

    return predictions

