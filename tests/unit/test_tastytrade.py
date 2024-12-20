from tastytrade_ghostfolio.main import (
    adapt_symbol_changes,
    extract_symbol_changes,
    filter_trades,
)


class TestFilterTrades:
    def test_should_filter_dividend_reinvestments(
        self, transactions, dividend_reinvestment_transaction_buy
    ):
        result = filter_trades(transactions)

        assert dividend_reinvestment_transaction_buy in result

    def test_should_filter_buy_trades(self, transactions, trade_buy):
        result = filter_trades(transactions)

        assert trade_buy in result

    def test_should_filter_symbol_changes(
        self, transactions, symbol_change_sell_old, symbol_change_buy_new
    ):
        result = filter_trades(transactions)

        assert symbol_change_sell_old in result
        assert symbol_change_buy_new in result


class TestExtractSymbolChanges:
    def test_when_theres_symbol_change_should_return_transactions_and_changes_separately(
        self, transactions, symbol_changeless_transactions, symbol_change
    ):
        clean_transactions, symbol_changes = extract_symbol_changes(transactions)

        assert clean_transactions == symbol_changeless_transactions
        assert symbol_changes == symbol_change

    def test_when_theres_no_symbol_change_should_return_all_transactions_and_empty_list(
        self, symbol_changeless_transactions
    ):
        clean_transactions, symbol_changes = extract_symbol_changes(
            symbol_changeless_transactions
        )

        assert clean_transactions == symbol_changeless_transactions
        assert symbol_changes == []


class TestAdaptSymbolChanges:
    def test_should_map_old_symbol_to_new_one(
        self, symbol_changeless_transactions, symbol_change
    ):
        result = adapt_symbol_changes(symbol_changeless_transactions, symbol_change)

        assert all(
            transaction.symbol == "COLA"
            for transaction in result
            if transaction.transaction_sub_type == "Dividend"
        )
