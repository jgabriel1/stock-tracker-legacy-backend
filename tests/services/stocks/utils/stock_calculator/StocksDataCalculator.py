from typing import List, Mapping, AbstractSet, MutableMapping

from .StockPerTickerCalculator import StockPerTickerCalculator
from .TransactionPerTickerSeparator import TransactionPerTickerSeparator
from ...entities import Transaction, Stock


class StocksDataCalculator:
    transactions_data: List[Transaction]
    stocks_data: MutableMapping[str, Stock]

    _separated_transactions: Mapping[str, List[Transaction]]
    _tickers: AbstractSet[str]

    def __init__(self, transactions_data: List[Transaction]):
        self.transactions_data = transactions_data
        self.stocks_data = {}

        self._separate_transactions()
        self._tickers = self._separated_transactions.keys()

    def _separate_transactions(self) -> None:
        separator = TransactionPerTickerSeparator(self.transactions_data)
        self._separated_transactions = separator.separate_transactions()

    def calculate_stocks(self) -> MutableMapping[str, Stock]:
        for ticker in self._tickers:
            transactions = self._separated_transactions.get(ticker)
            calculator = StockPerTickerCalculator(transactions, ticker)

            calculated_stock = calculator.calculated()
            if not calculated_stock.is_empty():
                self.stocks_data.update({ticker: calculated_stock})

        return self.stocks_data
