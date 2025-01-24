from datetime import datetime
from decimal import Decimal

from tastytrade_ghostfolio.core.entity.split import Split
from tastytrade_ghostfolio.core.entity.trade import Trade


class Asset:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self._trades: list[Trade] = []

    @property
    def trades(self) -> list[Trade]:
        return self._trades

    def add_trades(self, trades: list[Trade]):
        self._trades += trades
        self._trades = sorted(self._trades, key=lambda x: x.executed_at)

    def split_shares(self, split: Split):
        before_the_fact_trades = list(
            filter(lambda x: x.executed_at.date() <= split.effective_date, self._trades)
        )
        for trade in before_the_fact_trades:
            trade.quantity = trade.quantity * split.ratio
            trade.unit_price = trade.unit_price / split.ratio

    def has_trade(self, trade: Trade) -> bool:
        return any(
            _trade.executed_at.date() == trade.executed_at.date()
            and _trade.quantity == trade.quantity
            and _trade.symbol == trade.symbol
            and _trade.unit_price == trade.unit_price
            for _trade in self._trades
        )

    def get_trade(
        self, executed_at: datetime, quantity: Decimal, symbol: str, unit_price: Decimal
    ) -> Trade:
        return next(
            filter(
                lambda x: x.executed_at == executed_at
                and x.quantity == quantity
                and x.symbol == symbol
                and x.unit_price == unit_price,
                self._trades,
            )
        )

    def delete_trade(self, trade: Trade):
        _trade = self.get_trade(
            trade.executed_at, trade.quantity, trade.symbol, trade.unit_price
        )

        self._trades.remove(_trade)

    def change_symbol(self, symbol: str):
        self.symbol = symbol
        for trade in self._trades:
            trade.symbol = symbol
