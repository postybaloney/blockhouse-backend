import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from .models import StockData
from sklearn.metrics import mean_absolute_error
import io
import base64
import matplotlib.pyplot as plt

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
        stock_data, created = StockData.objects.update_or_create(
            symbol=symbol,
            date = pd.Timestamp.now() + pd.Timedelta(days=i+1), # Simulate future days
            defaults={
                'open_price': 0,
                'high_price': 0,
                'low_price': 0,
                'volume': 0,
                'close_price':next_pred,
                'is_predicted': True, # Tells this is a prediction
            }
        )

    return predictions

def calculate_prediction_metrics(actual_prices, predicted_prices):
    """
    Find the Mean Absolute Error for the model's predictions
    """
    mae = mean_absolute_error(actual_prices, predicted_prices)

    return {
        'MAE': mae,
        'Total Predictions': len(predicted_prices)
    }

def generate_stock_price_plot(actual_prices, predicted_prices, dates, symbol):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, actual_prices, label='Actual Prices', color='blue')
    plt.plot(dates, predicted_prices, label='Predicted Prices', color='orange')
    plt.title(f'Actual vs Predicted Prices for {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    plt.savefig('stock_price_comparison.png')
    plt.close()

# In stocks/ML.py
def generate_visualization(symbol, days):
    # Fetch the actual stock prices for the given symbol and days
    df = get_data(symbol, days)

    # Assuming you have a function for making predictions, get predictions here
    predicted_prices = predict_prices(symbol, days)

    # Call the existing plotting function to generate the plot
    actual_prices = df['close_price'].values
    dates = df['date'].dt.strftime('%Y-%m-%d').values  # Format dates for x-axis

    # Generate the stock price plot
    generate_stock_price_plot(actual_prices, predicted_prices, dates, symbol)

    # Return base64 encoding of the saved image (optional)
    with open('stock_price_comparison.png', "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

    return encoded_string  # Return the encoded string if needed