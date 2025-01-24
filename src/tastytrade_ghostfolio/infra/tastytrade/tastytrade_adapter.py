from decimal import Decimal
from itertools import batched
from typing import Iterable

from tastytrade.account import Transaction

from tastytrade_ghostfolio.core.entity.split import Split
from tastytrade_ghostfolio.core.entity.symbol_change import SymbolChange
from tastytrade_ghostfolio.core.entity.trade import Trade
from tastytrade_ghostfolio.core.entity.transaction_type import TransactionType
from tastytrade_ghostfolio.core.ports.tastytrade import TastytradePort
from tastytrade_ghostfolio.infra.tastytrade.tastytrade_api import TastytradeApi

TRADE_TYPE_MAPPING = {
    "Buy to Open": TransactionType.BUY,
    "Sell to Close": TransactionType.SELL,
}


class TastytradeAdapter(TastytradePort):
    def __init__(self, tastytrade_api: TastytradeApi):
        self._tastytrade_api = tastytrade_api
        self._history = self._get_transaction_history()

    def _get_transaction_history(self) -> list[Transaction]:
        return self._tastytrade_api.get_trades_history()

    def get_trades(self, asset: str | None = None) -> list[Trade]:
        transactions = self._filter_trades(asset)
        return list(map(self._adapt_trade, transactions))

    @staticmethod
    def _adapt_trade(transaction: Transaction) -> Trade:
        fee = TastytradeAdapter._calculate_total_fee(
            transaction.clearing_fees,
            transaction.commission,
            transaction.proprietary_index_option_fees,
            transaction.regulatory_fees,
        )

        return Trade(
            description=transaction.description,
            executed_at=transaction.executed_at,
            fee=fee,
            quantity=transaction.quantity,
            symbol=transaction.symbol,
            transaction_type=TRADE_TYPE_MAPPING[transaction.action],
            unit_price=transaction.price,
        )

    @staticmethod
    def _calculate_total_fee(
        clearing_fee: Decimal | None,
        commission: Decimal | None,
        proprietary_index_option_fees: Decimal | None,
        regulatory_fee: Decimal | None,
    ) -> Decimal:
        clearing_fee = Decimal("0.0") if clearing_fee is None else clearing_fee
        commission = Decimal("0.0") if commission is None else commission
        proprietary_index_option_fees = (
            Decimal("0.0")
            if proprietary_index_option_fees is None
            else proprietary_index_option_fees
        )
        regulatory_fee = Decimal("0.0") if regulatory_fee is None else regulatory_fee

        return abs(
            clearing_fee + commission + proprietary_index_option_fees + regulatory_fee
        )

    def _filter_trades(self, asset: str | None = None) -> Iterable[Transaction]:
        transactions = filter(lambda x: x.transaction_type == "Trade", self._history)
        if asset:
            return filter(lambda x: x.symbol == asset, transactions)

        return transactions

    def get_assets(self) -> list[str]:
        trades = self.get_trades()
        trades = set(map(lambda x: x.symbol, trades))

        dividends = self.get_dividends()
        dividends = set(map(lambda x: x.symbol, dividends))

        return list(trades | dividends)

    def get_symbol_changes(self) -> list[SymbolChange]:
        transactions = self._filter_symbol_changes()
        transactions = sorted(transactions, key=lambda x: x.transaction_date)

        symbol_changes = []
        for changes in batched(transactions, 2):
            old_symbol = next(filter(lambda x: x.action == "Sell to Close", changes))
            new_symbol = next(filter(lambda x: x.action == "Buy to Open", changes))
            symbol_changes.append(
                SymbolChange(old_symbol=old_symbol.symbol, new_symbol=new_symbol.symbol)
            )

        return symbol_changes

    def _filter_symbol_changes(self) -> Iterable[Transaction]:
        return filter(
            lambda x: x.transaction_type == "Receive Deliver"
            and x.transaction_sub_type == "Symbol Change",
            self._history,
        )

    def get_splits(self) -> list[Split]:
        transactions = self._filter_splits()
        transactions = sorted(transactions, key=lambda x: x.transaction_date)

        splits = []
        for split_specifications in batched(transactions, 2):
            sell_transaction = next(
                filter(lambda x: x.action == "Sell to Close", split_specifications)
            )
            buy_transaction = next(
                filter(lambda x: x.action == "Buy to Open", split_specifications)
            )

            split_ratio = buy_transaction.quantity / sell_transaction.quantity

            splits.append(
                Split(
                    effective_date=buy_transaction.transaction_date,
                    ratio=split_ratio,
                    symbol=buy_transaction.symbol,
                )
            )

        return splits

    def _filter_splits(self) -> Iterable[Transaction]:
        return filter(
            lambda x: x.transaction_type == "Receive Deliver"
            and x.transaction_sub_type == "Forward Split",
            self._history,
        )

    def get_dividends(self, asset: str | None = None) -> list[Trade]:
        transactions = self._filter_dividends(asset)
        return list(map(self._adapt_trade, transactions))

    def _filter_dividends(self, asset: str | None = None) -> Iterable[Transaction]:
        transactions = filter(
            lambda x: x.transaction_type == "Receive Deliver"
            and x.transaction_sub_type == "Dividend",
            self._history,
        )

        if asset:
            return filter(lambda x: x.symbol == asset, transactions)

        return transactions
