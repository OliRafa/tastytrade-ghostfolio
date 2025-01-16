from tastytrade_ghostfolio.services.tastytrade import TastytradeService


class TestFilterTrades:
    def test_should_filter_dividend_reinvestments(
        self, transactions, dividend_reinvestment_transaction_buy
    ):
        result = TastytradeService._filter_trades(transactions)

        assert dividend_reinvestment_transaction_buy in result

    def test_should_filter_buy_trades(self, transactions, trade_buy):
        result = TastytradeService._filter_trades(transactions)

        assert trade_buy in result

    def test_should_filter_symbol_changes(
        self, transactions, symbol_change_sell_old, symbol_change_buy_new
    ):
        result = TastytradeService._filter_trades(transactions)

        assert symbol_change_sell_old in result
        assert symbol_change_buy_new in result
