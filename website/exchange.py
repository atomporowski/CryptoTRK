import config
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from binance.client import Client
import pygal
from pygal.style import NeonStyle

import os

exchange = Blueprint('portfolio', __name__)

# Connecting to the DB
# TODO : WHY DOES IT NOT WORK?!?!?!?
# engine = create_engine('sqlite:///database.db')
# connection = engine.connect()
# stmt = 'SELECT * FROM user'
# results = connection.execute(stmt).fetchall

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
    # Getting logged in user's email
    user123 = session['email']
    # getting current btc value to USD
    btc_info = client.get_symbol_ticker(symbol="BTCUSDT")
    btc_price = btc_info['price']
    btc_values = []
    graph = pygal.StackedLine(fill=True, interpolate='cubic', style=NeonStyle)
    graph.title = 'Portfolio value change overtime.'
    if user123 == 'adam.tomporowski@gmail.com':
        # dates = ['10.06', '11.06', '12.06']
        # graph.x_labels = dates
        values = [1232, 1247, 1240, 1275, 1260, 1253, 1177, 1156, 1208, 1153, 1120, 1136, 1132, 1175, 1363, 1416, 1411,
                  1536, 1601, 1607, 1598, 1642, 1539, 1648, 1620, 1626, 1659, 1650, 1543, 1607, 1402, 1451, 1506, 1394,
                  1414, 1322, 1353, 951, 1081, 922, 859, 740, 921, 919, 1020, 965, 857, 808, 866, 935, 920, 959, 1022,
                  938, 916, 936, 852, 843, 896, 851, 825]
        # Converting portfolio value to BTC
        for i in values:
            btc_value = i / float(btc_price)
            btc_values.append(btc_value)
    else:
        # dates = ['10.06', '11.06', '12.06']
        # graph.x_labels = dates
        values = [1000]
        for i in values:
            btc_value = i / float(btc_price)
            btc_values.append(btc_value)
    graph.add('USD', values)
    graph.add('BTC', btc_values, secondary=True)
    graph_data = graph.render_data_uri()
    return render_template("portfolio.html", user=current_user, my_balances=balance, portfolio=update_portfolio(),
                           current_prices=current_prices, graph_data=graph_data)


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

