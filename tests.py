import pytest, time, config
from binance.client import Client
from website.exchange import client

client = Client(config.apiKey, config.apiSecret)


class TestAPIConnection:

    def test_time_syn(self):
        local_time1 = int(time.time() * 1000)
        server_time = client.get_server_time()
        diff1 = server_time['serverTime'] - local_time1
        assert diff1 <= 5000

    def test_ping(self):
        response = client.ping()
        assert response == {}

    def test_adding_two_numbers(self):
        the_sum = 2 + 2
        assert the_sum == 4

    def test_price_change(self):
        symbol_info = client.get_avg_price(symbol='BTCUSDT')
        entry = float(50000)
        difference = float(symbol_info['price']) - entry
        assert difference != 0


