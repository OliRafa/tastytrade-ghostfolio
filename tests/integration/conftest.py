import datetime
from decimal import Decimal

from pytest import fixture

from tastytrade_ghostfolio.core.entity.trade import Trade
from tastytrade_ghostfolio.core.entity.transaction_type import TransactionType


@fixture
def stock_a_trades() -> list[Trade]:
    return [
        Trade(
            executed_at=datetime.datetime(
                2023, 9, 27, 18, 36, 20, 28000, tzinfo=datetime.timezone.utc
            ),
            fee=Decimal("0.001"),
            quantity=Decimal("1.0"),
            symbol="STOCKA",
            transaction_type=TransactionType.BUY,
            unit_price=Decimal("40.3989"),
        ),
        Trade(
            executed_at=datetime.datetime(
                2023, 9, 27, 18, 36, 20, 28000, tzinfo=datetime.timezone.utc
            ),
            fee=Decimal("0.001"),
            quantity=Decimal("2.0"),
            symbol="STOCKA",
            transaction_type=TransactionType.BUY,
            unit_price=Decimal("41.3989"),
        ),
        Trade(
            executed_at=datetime.datetime(
                2023, 9, 27, 18, 36, 20, 28000, tzinfo=datetime.timezone.utc
            ),
            fee=Decimal("0.001"),
            quantity=Decimal("3.0"),
            symbol="STOCKA",
            transaction_type=TransactionType.BUY,
            unit_price=Decimal("42.3989"),
        ),
    ]


@fixture
def stock_b_trades(stock_a_trades) -> list[Trade]:
    trades = [trade.model_copy() for trade in stock_a_trades]
    for trade in trades:
        trade.symbol = "STOCKB"

    return trades
