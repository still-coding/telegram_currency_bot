import json
from time import time

import grequests
import redis

from exceptions import DataFetchError


class ExchangeRatesParser:
    """Exchange rates parsing from CoinGecko API V3 static class.
    API docs: https://www.coingecko.com/en/api/documentation

    Rates format:
    {
        'ticker': {
            'name": str,
            'unit': str,
            'value': float,
            'type': str
        },
        ...
    }
    """

    urls = (
        "https://api.coingecko.com/api/v3/ping",
        "https://api.coingecko.com/api/v3/exchange_rates",
    )
    redis_connection = redis.Redis(host="redis", port=6379)

    @classmethod
    def __parse_rates(cls):
        """Async parsing private method. Caches results in redis.

        Raises:
            DataFetchError: if connection failed.

        Returns:
            None
        """
        responses = grequests.map((grequests.get(link) for link in cls.urls))
        if not responses[0].ok:
            raise DataFetchError("Connection to Coingecko API failed.")
        rates = responses[1].content
        cls.redis_connection.set("rates", rates)
        cls.redis_connection.set("timestamp", time())

    @classmethod
    def get_rates(cls):
        """Calls parse method if there are no rates or rates older than one minute.
        Returns cached rates otherwise.

        Raises:
            DataFetchError: if fetched data does not contains rates data.

        Returns:
            tickers_to_units (dict): maps tickers to its units (e.g. 'eur': '€'),
            rates (dict): rates fetched from API.
        """
        try:
            timestamp = cls.redis_connection.get("timestamp")
        except redis.exceptions.ConnectionError:
            raise DataFetchError("Failed to establish connection with redis")
        if not timestamp or time() - float(timestamp) > 60.0:
            cls.__parse_rates()
        rates = json.loads(cls.redis_connection.get("rates"))
        if not (isinstance(rates, dict) and "rates" in rates):
            raise DataFetchError("Failed to retrieve exchange rates from Coingecko API")
        rates = rates["rates"]
        tickers_to_units = {ticker: data.get("unit") for ticker, data in rates.items()}
        return tickers_to_units, rates
