import config
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from binance.client import Client
from .models import User, Portfolios
import os
from sqlalchemy import select
import pandas as pd
from . import db
from matplotlib import pyplot as plt

exchange = Blueprint('portfolio', __name__)

portfolio = []
current_prices = []
historical_symbols = []

# Path to pictograms folder
pictograms_folder = os.path.join('static', 'pictograms')

# Connecting to binance api
client = Client(config.apiKey, config.apiSecret)

# Getting all current assets info
acc_info = client.get_account()
# Gets info about amount of each coin owned
balance = acc_info['balances']


@exchange.route('/portfolio', methods=['GET', 'POST'])
@login_required
def exchange_page():
    # performance_graphs()
    user123 = 1231241241241

    return render_template("portfolio.html", user=current_user, my_balances=balance, portfolio=update_portfolio(),
                           current_prices=current_prices, user123=user123)


def update_portfolio():
    portfolio = []
    prices = []
    current_prices = client.get_all_tickers()
    print("BALANCE", balance)
    for b in balance:
        if float(b['free']) > 0 or float(b['locked']) > 0:
            portfolio.append(b)
            symbol = b['asset'] + 'USDT'
            for i in current_prices:
                if (symbol == i['symbol']):
                    price = i['price']
                    p = [{'asset': b['asset'], "free": b['free'], "locked": b["locked"], 'price': price}]
                    for v in p:
                        if v['asset'] == b['asset']:
                            prices.append(v)

    return prices


def get_trades_history():
    trades = client.get_historical_trades(symbol='FIOUSDT')
    print(trades)


def performance_graphs():
    select = 'SELECT user.id FROM user'
    user123 = User.query.get(id(current_user))
    return user123
