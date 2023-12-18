from datetime import date

from tastytrade_ghostfolio.adapters.trade import _adapt_trade
from tastytrade_ghostfolio.models.ghostfolio_activity import (
    GhostfolioActivity,
    TransactionType,
)


def test_adapt_trade_should_adapt_buy_trade(trade_buy):
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
