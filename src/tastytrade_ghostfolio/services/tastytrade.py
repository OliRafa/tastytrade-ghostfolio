from tastytrade import Account, Session
from tastytrade.account import Transaction

from tastytrade_ghostfolio.configs.settings import Settings


class TastytradeService:
    def __init__(self):
        self._session = self._get_session()
        self._account = self._get_account()

    def _get_session(self) -> Session:
        return Session(Settings.Tastytrade.USERNAME, Settings.Tastytrade.PASSWORD)

    def _get_account(self) -> Account:
        return Account.get_accounts(self._session)[0]

    def get_trades_history(self) -> list[Transaction]:
        return self._filter_trades(self._account.get_history(self._session))

    @staticmethod
    def _filter_trades(transactions: list[Transaction]) -> list[Transaction]:
        trades = []
        for transaction in transactions:
            if transaction.transaction_type == "Trade" or (
                transaction.transaction_type == "Receive Deliver"
                and (
                    transaction.transaction_sub_type == "Dividend"
                    or transaction.transaction_sub_type == "Symbol Change"
                    or transaction.transaction_sub_type == "Forward Split"
                )
            ):
                trades.append(transaction)

        return trades
