class CurrencyConverter:
    """Converter class. Uses rates fetched by ExchangeRatesParser."""

    def __init__(self, rates):
        """Converter initializer.

        Args:
            rates (dict): exchange rates in following format:
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
        self.rates = rates

    def convert(self, amount, from_curr, to_curr):
        """Single conversion method.

        Args:
            amount (float): amount of source currency (from_curr),
            from_curr (str): ticker of source currency,
            to_curr (str): ticker of destination currency.

        Returns:
            float: amount of destination currency (to_curr)
        """
        if from_curr == "btc":
            return self.rates[to_curr]["value"] * amount
        return self.rates[to_curr]["value"] / self.rates[from_curr]["value"] * amount
