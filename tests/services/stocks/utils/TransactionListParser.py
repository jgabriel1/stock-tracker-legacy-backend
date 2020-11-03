from typing import List

from ..entities import Transaction


class TransactionListParser:
    _raw_transactions: List[dict]

    def __init__(self, transactions: List[dict]):
        self._raw_transactions = transactions

    def get_parsed(self) -> List[Transaction]:
        return [
            Transaction.parse_obj(transaction)
            for transaction in self._raw_transactions
        ]
