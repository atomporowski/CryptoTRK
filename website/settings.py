from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Portfolios
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

settings = Blueprint('settings', __name__)


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    flash('Remember to set your api as read only via Binance settings!', category='error')
    if request.method == 'POST':
        api_key = request.form.get('apiKey')
        api_secret = request.form.get('apiSecret')

        if len(api_key) != 64 or len(api_secret) != 64:
            flash('apiKey  or apiSecret is not correct!', category='error')
        else:
            new_portfolio = Portfolios(apiKey=api_key, apiSecret=api_secret, user_id=current_user.id)
            db.session.add(new_portfolio)
            db.session.commit()
            flash('Connected with api successfully', category='success')
    return render_template("settings.html", user=current_user)


# TODO : List all the apis already added