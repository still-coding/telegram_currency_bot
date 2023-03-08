from string import ascii_lowercase

import pymorphy2

from config import NAMES_TO_TICKERS

from exceptions import UserQueryParsingError


class UserQueryParser:
    """User input parser. Non-static, so one needs to create an instance to use it."""

    def __init__(self, ticker_list, tickers_to_units):
        """Parser initializer.

        Args:
            ticker_list (iterable): collection of currency tickers,
            tickers_to_units (dict): ticker-unit mapping (e.g. 'eur': '€').
        """
        self.ticker_list = ticker_list
        self.tickers_to_units = tickers_to_units
        self.__morph = pymorphy2.MorphAnalyzer()
        self.__normalize_russian = lambda word: self.__morph.parse(word)[0].normal_form

    def __parse_ticker(self, currency_name):
        """_summary_

        Args:
            currency_name (_type_): _description_

        Raises:
            UserInputParsingError: _description_

        Returns:
            _type_: _description_
        """
        # normalize if russian
        if any(map(lambda x: x not in ascii_lowercase, currency_name)):
            currency_name = self.__normalize_russian(currency_name)
        # check if in predefined names
        for names, ticker in NAMES_TO_TICKERS.items():
            if currency_name in names:
                return ticker
        # check if in list of available tickers
        if currency_name in self.ticker_list:
            return currency_name
        # check if in available units
        for ticker, unit in self.tickers_to_units.items():
            if currency_name == unit:
                return ticker
        raise UserQueryParsingError(f"Failed to figure out ticker for {currency_name}")

    def parse(self, query):
        """Parses user query. Query must be in the form "x from_ticker to|в to_ticker" to parse it.

        Args:
            query (str): user query string.

        Raises:
            UserQueryParsingError: if there is an error during parsing

        Returns:
            amount (float): source currency amount,
            from_currency (str): source currency ticker,
            to_currency (str): destination currency ticker.
        """
        match query.strip().lower().replace(",", ".").split():
            case (str(amount), str(from_currency), "в" | "to", str(to_currency)):
                try:
                    amount = float(amount)
                except ValueError:
                    raise UserQueryParsingError(f"Failed to convert {amount} to float")
            case _:
                raise UserQueryParsingError(f"Failed to parse query: {query}")

        from_currency = self.__parse_ticker(from_currency)
        to_currency = self.__parse_ticker(to_currency)
        return amount, from_currency, to_currency
