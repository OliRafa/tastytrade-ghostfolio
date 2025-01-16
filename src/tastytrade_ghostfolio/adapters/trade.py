from tastytrade.account import Transaction

from tastytrade_ghostfolio.models.ghostfolio_activity import (
    GhostfolioActivity,
    TransactionType,
)

TRADE_TYPE_MAPPING = {
    "Buy to Open": TransactionType.BUY,
    "Sell to Close": TransactionType.SELL,
}


def adapt_trades(trades: list[Transaction]) -> list[GhostfolioActivity]:
    adapted_trades = []

    for trade in trades:
        adapted_trades.append(_adapt_trade(trade))

    return adapted_trades


def _adapt_trade(trade: Transaction) -> GhostfolioActivity:
    return GhostfolioActivity(
        currency="USD",
        date=trade.transaction_date,
        fee=abs(float(trade.clearing_fees)) if trade.clearing_fees else 0.0,
        quantity=float(trade.quantity),
        symbol=trade.symbol,
        type=TRADE_TYPE_MAPPING[trade.action],
        unit_price=float(trade.price),
    )
