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
