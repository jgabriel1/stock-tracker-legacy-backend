from typing import List

from ...entities import Transaction, Stock


class StockPerTickerCalculator:
    transactions_list: List[Transaction]
    ticker: str

    _total_invested: float
    _total_shares_bought: int
    _total_shares_sold: int

    _currently_owned_shares: int
    _average_bought_price: float

    def __init__(self, transactions_list: List[Transaction], ticker: str):
        self.transactions_list = transactions_list
        self.ticker = ticker

        self._total_invested = 0
        self._total_shares_bought = 0
        self._total_shares_sold = 0

        self._calculate()

    def _calculate(self) -> None:
        for transaction in self.transactions_list:
            if transaction.quantity > 0:
                self._total_invested += transaction.total_value
                self._total_shares_bought += abs(transaction.quantity)
            else:
                self._total_shares_sold += abs(transaction.quantity)

    @property
    def _currently_owned_shares(self) -> int:
        return self._total_shares_bought - self._total_shares_sold

    @property
    def _average_bought_price(self) -> float:
        return self._total_invested / self._total_shares_bought

    def calculated(self) -> Stock:
        return Stock.parse_obj({
            'ticker': self.ticker,
            'currently_owned_shares': self._currently_owned_shares,
            'average_bought_price': self._average_bought_price,
        })
