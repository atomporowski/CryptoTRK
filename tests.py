import pytest
from binance.client import Client
import config

import website.exchange
from website.exchange import client


class TestExchangeOperations:

    def test_api_connection(self):
        client = Client(config.apiKey, config.apiSecret)
        assert client


client = Client(config.apiKey, config.apiSecret)
print(client)
