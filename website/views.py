from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from pycoingecko import CoinGeckoAPI
import time, datetime, sched

views = Blueprint('views', __name__)

# Connecting to CoinGecko
cg = CoinGeckoAPI()

prices = cg.get_price(
    ids='bitcoin, ethereum, binancecoin, cardano, dogecoin, ripple, polkadot, uniswap, solana, litecoin',
    vs_currencies=['usd', 'pln'], include_market_cap='true', include_24hr_change='true',
    include_last_updated_at='true')

# TODO : Done with JS but I want to try with python if I got some time
# sorting by market cap
# {k: v for k, v in sorted(prices.items(), key=lambda item: item[1])}
# sorted(prices, key=lambda e: (-e['usd_market_cap'], e['i']))


# Converting time
date = time.time()
last_synch = prices['bitcoin']['last_updated_at']
last_synch_readable = (datetime.datetime.fromtimestamp(int(last_synch)).strftime('%Y-%m-%d %H:%M:%S'))


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    prices = cg.get_price(
        ids='bitcoin, ethereum, binancecoin, cardano, dogecoin, ripple, polkadot, uniswap, solana, litecoin',
        vs_currencies=['usd', 'pln'], include_market_cap='true', include_24hr_change='true',
        include_last_updated_at='true')
    return render_template("home.html", user=current_user, prices=prices, last_synch=last_synch_readable)


# Synchronizing prices every few minutes
# def force_synchronization():
#    starttime = time.time()
#    while True:
#        prices = cg.get_price(
#            ids='bitcoin, ethereum, binancecoin, cardano, dogecoin, ripple, polkadot, uniswap, solana, litecoin',
#            vs_currencies=['usd', 'pln'], include_market_cap='true', include_24hr_change='true',
#            include_last_updated_at='true')
#        time.sleep(60.0 - ((time.time() - starttime) % 60.0))
#
#    return prices


# Synchronizing prices on every page load
#def force_synchronization():
#    prices = cg.get_price(
#        ids='bitcoin, ethereum, binancecoin, cardano, dogecoin, ripple, polkadot, uniswap, solana, litecoin',
#        vs_currencies=['usd', 'pln'], include_market_cap='true', include_24hr_change='true',
#        include_last_updated_at='true')
#
#    return prices
