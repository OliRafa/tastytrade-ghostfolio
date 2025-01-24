from tastytrade.account import Transaction

from tests.resources.tastytrade.tastytrade_transactions import TRANSACTIONS


class InMemoryTastytradeApi:
    def __init__(self):
        self._trades = TRANSACTIONS

    def get_trades_history(self) -> list[Transaction]:
        return self._trades
