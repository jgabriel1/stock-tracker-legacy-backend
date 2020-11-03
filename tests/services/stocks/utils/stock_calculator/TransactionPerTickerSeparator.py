from typing import Mapping, List, MutableMapping

from ...entities import Transaction


class TransactionPerTickerSeparator:
    transactions_data: List[Transaction]
    transactions_mapping: MutableMapping[str, List[Transaction]]

    def __init__(self, transactions_data: List[Transaction]):
        self.transactions_data = transactions_data
        self.transactions_mapping = {}

    def separate_transactions(self) -> Mapping[str, List[Transaction]]:
        for transaction in self.transactions_data:
            ticker = transaction.ticker

            try:
                self.transactions_mapping.update({
                    ticker: [*self.transactions_mapping[ticker], transaction]
                })
            except KeyError:
                self.transactions_mapping.update({
                    ticker: [transaction]
                })

        return self.transactions_mapping
