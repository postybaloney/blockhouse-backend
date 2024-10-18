from django.shortcuts import render
from django.http import JsonResponse
from .api import fetch_stock_data

# Create your views here.
def update_stock_data(request, symbol):
    try:
        fetch_stock_data(symbol=symbol)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'Status': 'Error', 'Message': str(e)}, status=500)