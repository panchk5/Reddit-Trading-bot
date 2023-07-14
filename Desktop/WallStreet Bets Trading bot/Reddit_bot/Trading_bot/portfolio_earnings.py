from django.shortcuts import render
import alpaca_trade_api as tradeapi


def portfolio_earnings(request):
    api_key = "PKAI4GTFN5H2U9P1MYWC"
    secret = "1Zr0NmxMfugVdloccntM0HGatOzwFPoRaF2EZ0NY"
    base_url = 'https://paper-api.alpaca.markets'

    api = tradeapi.REST(api_key, secret, base_url, api_version='v2')


    # Retrieve portfolio information
    account = api.get_account()
    portfolio = api.list_positions()
    earning = 0
    for position in portfolio:
        symbol = position.symbol
        cost_basis = float(position.cost_basis)
        quantity = int(position.qty)
        current_price = api.get_last_trade(symbol).price

        position_value = current_price * quantity
        position_earnings = position_value - (cost_basis * quantity)
        earnings += position_earnings
    context = {
        'earnings': earnings,
        'portfolio': portfolio,
    }
    return render(request, 'generic.html', context)