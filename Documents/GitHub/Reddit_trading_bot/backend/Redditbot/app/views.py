from django.shortcuts import render
import alpaca_trade_api as tradeapi
# Create your views here.
from rest_framework import generics
# from .models import Earning
# from .serializers import EarningSerializer
from django.http import JsonResponse


# class EarningList(generics.ListCreateAPIView):
#     queryset = Earning.objects.all()
#     serializer_class = EarningSerializer

# def portfolio_earnings(request):
#     # earnings = Earning.objects.all()
#     api_key = "PKAI4GTFN5H2U9P1MYWC"
#     secret = "1Zr0NmxMfugVdloccntM0HGatOzwFPoRaF2EZ0NY"
#     base_url = 'https://paper-api.alpaca.markets'

#     api = tradeapi.REST(api_key, secret, base_url, api_version='v2')


#     # Retrieve portfolio information
#     account = api.get_account()
#     portfolio = api.list_positions()
#     earnings = 0
#     for position in portfolio:
#         symbol = position.symbol
#         cost_basis = float(position.cost_basis)
#         quantity = int(position.qty)
#         current_price = api.get_latest_trade(symbol).price

#         position_value = current_price * quantity
#         position_earnings = position_value - (cost_basis * quantity)
#         earnings += position_earnings
#     context = {
#         'earnings': earnings,
#         'portfolio': portfolio,
#     }
#     return JsonResponse(context, safe=False)

def portfolio_earnings(request):
    api_key = "PKAI4GTFN5H2U9P1MYWC"
    secret = "1Zr0NmxMfugVdloccntM0HGatOzwFPoRaF2EZ0NY"
    base_url = 'https://paper-api.alpaca.markets'

    api = tradeapi.REST(api_key, secret, base_url, api_version='v2')

    # Retrieve portfolio information
    account = api.get_account()
    portfolio = api.list_positions()

    earnings = 0
    portfolio_data = []

    for position in portfolio:
        symbol = position.symbol
        cost_basis = float(position.cost_basis)
        quantity = int(position.qty)
        current_price = api.get_latest_trade(symbol).price

        position_value = current_price * quantity
        position_earnings = position_value - (cost_basis)
        earnings += position_earnings

        # Create a dictionary with relevant position information
        position_info = {
            'symbol': symbol,
            'quantity': quantity,
            'current_price': current_price,
            'position_earnings': position_earnings
        }
        portfolio_data.append(position_info)

    context = {
        'earnings': earnings,
        'portfolio': portfolio_data  # Use the serializable portfolio data
    }

    return JsonResponse(context, safe=False)

def front(request):
    context = {}
    return render(request, 'index.html', context)