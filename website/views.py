from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from pycoingecko import CoinGeckoAPI
import json, datetime

views = Blueprint('views', __name__)

# Connecting to CoinGecko
cg = CoinGeckoAPI()

prices = cg.get_price(
    ids=['bitcoin', 'ethereum', 'binancecoin', 'dogecoin', 'cardano', 'ripple', 'polkadot', 'uniswap', 'solana', 'litecoin'],
    vs_currencies='usd')


print(cg.get_coins_list())

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user, prices=prices)
