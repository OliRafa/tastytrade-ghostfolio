from tastytrade_ghostfolio.main import filter_trades


def test_filter_trades_should_filter_dividend_reinvestments(
    transactions, dividend_reinvestment_transaction_buy
):
    result = filter_trades(transactions)

    assert len(result) == 4
    assert dividend_reinvestment_transaction_buy in result


def test_filter_trades_should_filter_buy_trades(transactions, trade_buy):
    result = filter_trades(transactions)

    assert len(result) == 4
    assert trade_buy in result
