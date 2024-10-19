from django.shortcuts import render
from django.http import JsonResponse
from .api import fetch_stock_data
from .backtests import backtest_strategy
from .ML import predict_prices

# Create your views here.
def update_stock_data(request, symbol):
    try:
        fetch_stock_data(symbol=symbol)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'Status': 'Error', 'Message': str(e)}, status=500)
    
def backtest_view(request):
    symbol = request.GET.get('symbol', 'AAPL') # Defaults to AAPL
    initial_investment = float(request.GET.get('initial_investment', 10000))
    short_window = int(request.GET.get('short_window', 50))
    long_window = int(request.GET.get('long_window', 200))

    result = backtest_strategy(symbol=symbol, initial_investment=initial_investment, short_window=short_window, long_window=long_window)
    return JsonResponse(result)

def predict_view(request):
    symbol = request.GET.get('symbol', 'AAPL') # Defaults to AAPL
    days = int(request.GET.get('days', 30)) # Defualts to future 30 days

    predictions = predict_prices(symbol=symbol, days=days)

    return JsonResponse({
        'symbol': symbol,
        'Predictions': predictions.tolist()
    })