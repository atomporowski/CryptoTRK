import config
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from binance.client import Client
import pygal, time, datetime
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
values = []
current_coins = []

# Path to pictograms folder
pictograms_folder = os.path.join('static', 'pictograms')

# Connecting to binance api
client = Client(config.apiKey, config.apiSecret)

# Getting all current assets info
acc_info = client.get_account()
# Gets info about amount of each coin owned
balance = acc_info['balances']
# Getting current prices
current_prices = client.get_all_tickers()

# path = "./templates/static/pictograms/"
#
# for file in os.listdir(path):
#     os.rename(path + file, path + file.lower())

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
                           current_prices=current_prices, history=get_trades_history(prices=update_portfolio()),
                           graph_data=graph_data,
                           performance=calc_performance(trades=trades, curr_port=update_portfolio()))


def update_portfolio(current_prices=current_prices):
    portfolio = []
    prices = []
    # current_prices = client.get_all_tickers()
    # print(current_prices)
    # print("BALANCE", balance)
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


def get_trades_history(prices):
    symbols = []
    for i in prices:
        symbols.append(i['asset'] + 'USDT')
    trades = []
    for s in symbols:
        trades.extend(client.get_all_orders(symbol=s))
    for t in trades:
        t['time'] = (datetime.datetime.fromtimestamp(int(t['time']) / 1000).strftime('%Y-%m-%d %H:%M:%S'))
    # I was trying to remove canceled orders but the below fails for some reason
    # for y in range(51):
    #     if trades[y]['status'] == 'CANCELED':
    #         del trades[y]

    return trades


# Saving get_trades_history and coins owned to variables, we dont need to call API anymore
trades = get_trades_history(update_portfolio())


def calc_performance(trades, curr_port=update_portfolio()):
    avg_entries = []
    for i in curr_port:
        transacion_counter = 1
        money_spent_per_coin = 0.0
        avg_entry_price = 0.0
        if i['asset'] == 'USDT':
            continue
        price = client.get_all_orders(symbol=i['asset'] + 'USDT')
        # print(price)
        for y in price:
            if float(y['price']) == 0:
                continue
            if y['status'] == "FILLED" and y['side'] == "BUY":
                # money_per_transaction = (float(y['origQty']) * float(y['price']))
                money_per_transaction = (float(y['cummulativeQuoteQty']))
                avg_price_per_coin_in_this_transaction = float(y['cummulativeQuoteQty']) / float(y['origQty'])
                # print(money_per_transaction, avg_price_per_coin_in_this_transaction)
                money_spent_per_coin += money_per_transaction
                avg_entry_price = avg_entry_price + avg_price_per_coin_in_this_transaction
                transacion_counter = transacion_counter + 1
                # avg_entry_price = avg_entry_price / transacion_counter
        # print(money_spent_per_coin)
        coin_amount = (float(i['free']) + float(i['locked']))
        # print(i['asset'], "Coin owned: ", coin_amount, "Avg. entry price:", avg_entry_price / transacion_counter,
        #       "Trans counter: ", transacion_counter)
        avg_entries.append(
            {'symbol': i['asset'] + 'USDT', 'amount': coin_amount, 'avg': avg_entry_price / transacion_counter,
             'counter': transacion_counter, 'curr_price': i['price']})
    for i in avg_entries:
        if i['curr_price'] == i['avg']:
            i.update({'perc_change:': 0})
        elif i['avg'] != 0:
            i.update({'perc_change': ((float(i['curr_price'])) - float(i['avg'])) / float(i['avg']) * 100.0})
        else:
            i.update({'perc_change:': 'N/A'})

    return avg_entries


# def ping():
#     try:
#         client = Client(config.apiKey, config.apiSecret)
#         return client.ping()
#     except:
#         print("error")
#
#
# ping()
