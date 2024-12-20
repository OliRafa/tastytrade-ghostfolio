from datetime import date

from tastytrade_ghostfolio.adapters.trade import _adapt_trade
from tastytrade_ghostfolio.models.ghostfolio_activity import (
    GhostfolioActivity,
    TransactionType,
)


class TestAdaptTrade:
    def test_adapt_trade_should_adapt_buy_trade(self, trade_buy):
        expected_result = GhostfolioActivity(
            currency="USD",
            date=date(2023, 9, 27),
            fee=0.001,
            quantity=1.0,
            symbol="CCJ",
            type=TransactionType.BUY,
            unit_price=40.3989,
        )

        result = _adapt_trade(trade_buy)

        assert result == expected_result

    def test_adapt_trade_should_adapt_dividend_reinvestment(
        self,
        dividend_reinvestment_transaction_buy,
    ):
        expected_result = GhostfolioActivity(
            currency="USD",
            date=date(2023, 12, 15),
            fee=0.0,
            quantity=0.01391,
            symbol="KO",
            type=TransactionType.BUY,
            unit_price=59.04,
        )

        result = _adapt_trade(dividend_reinvestment_transaction_buy)

        assert result == expected_result

    def test_should_adapt_sell_on_symbol_change(self, symbol_change_sell_old):
        expected_result = GhostfolioActivity(
            currency="USD",
            date=date(2024, 7, 15),
            fee=0.0,
            quantity=5.47124,
            symbol="EURN",
            type=TransactionType.SELL,
            unit_price=15.01761940620408,
        )

        result = _adapt_trade(symbol_change_sell_old)

        assert result == expected_result

    def test_should_adapt_buy_on_symbol_change(self, symbol_change_buy_new):
        expected_result = GhostfolioActivity(
            currency="USD",
            date=date(2024, 7, 15),
            fee=0.0,
            quantity=5.47124,
            symbol="CMBT",
            type=TransactionType.BUY,
            unit_price=15.01761940620408,
        )

        result = _adapt_trade(symbol_change_buy_new)

        assert result == expected_result
