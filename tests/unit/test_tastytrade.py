# from tastytrade_ghostfolio.main import filter_dividends


# def test_filter_dividends_happy_path(transactions, dividends):
#     result = filter_dividends(transactions)

#     assert len(result) == 2
#     assert result == dividends
from tastytrade_ghostfolio.main import filter_trades


def test_filter_trades_should_filter_dividend_reinvestments(
    transactions, dividend_reinvestment_transaction_buy
):
    result = filter_trades(transactions)

    assert len(result) == 2
    assert dividend_reinvestment_transaction_buy in result


def test_filter_trades_should_filter_buy_trades(transactions, trade_buy):
    result = filter_trades(transactions)

    assert len(result) == 2
    assert trade_buy in result
