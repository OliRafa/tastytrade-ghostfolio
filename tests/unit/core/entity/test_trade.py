from datetime import datetime
from decimal import Decimal

from tastytrade_ghostfolio.core.entity.trade import Trade
from tastytrade_ghostfolio.core.entity.transaction_type import TransactionType
from tests.conftest import mark_test


class TestTrade:
    @mark_test
    def should_change_symbol(self):
        trade = Trade(
            executed_at=datetime.now(),
            fee=Decimal("0.0"),
            quantity=Decimal("0.0"),
            symbol="TEST",
            transaction_type=TransactionType.BUY,
            unit_price=Decimal("0.0"),
        )

        trade.change_symbol("NEW")
        assert trade.symbol == "NEW"

    @mark_test
    def when_dividend_has_unit_price_and_value_should_calculate_quantity(self):
        trade = Trade(
            executed_at=datetime.now(),
            fee=Decimal("0.0"),
            symbol="TEST",
            transaction_type=TransactionType.DIVIDEND,
            unit_price=Decimal("12.5"),
            value=Decimal("25.0"),
        )

        assert trade.quantity == Decimal("2.0")

    @mark_test
    def when_calculating_quantity_should_round_it_to_14_decimal_places(self):
        trade = Trade(
            executed_at=datetime.now(),
            fee=Decimal("0.21"),
            symbol="TEST",
            transaction_type=TransactionType.DIVIDEND,
            unit_price=Decimal("0.234"),
            value=Decimal("1.4"),
        )

        assert trade.quantity == Decimal("5.98290598290598")


class TestEquals:
    @mark_test
    def should_ignore_trailing_zeros_when_comparing(self):
        trade_a = Trade(
            executed_at=datetime.now(),
            fee=Decimal("0.210000"),
            symbol="TEST",
            transaction_type=TransactionType.DIVIDEND,
            unit_price=Decimal("0.234000"),
            value=Decimal("1.4"),
        )

        trade_b = Trade(
            executed_at=datetime.now(),
            fee=Decimal("0.21"),
            symbol="TEST",
            transaction_type=TransactionType.DIVIDEND,
            unit_price=Decimal("0.234"),
            value=Decimal("1.4"),
        )

        assert trade_a == trade_b
