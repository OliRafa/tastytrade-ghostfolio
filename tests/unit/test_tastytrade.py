import datetime
from decimal import Decimal

from tastytrade_ghostfolio.main import (
    adapt_symbol_changes,
    extract_forward_splits,
    extract_symbol_changes,
    filter_trades,
    get_split_specifications,
    split_shares,
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


class TestExtractForwardSplits:
    def test_when_theres_forward_splits_should_return_transactions_and_splits_separately(
        self, transactions, forward_split
    ):
        clean_transactions, forward_splits = extract_forward_splits(transactions)

        assert forward_splits == forward_split
        assert forward_split not in clean_transactions


class TestGetSplitSpecifications:
    def test_should_return_effective_date_and_split_ratio(
        self, forward_split, split_specifications
    ):
        result = get_split_specifications(forward_split)

        assert (
            result["CCJ"]["split_ratio"] == split_specifications["CCJ"]["split_ratio"]
        )
        assert (
            result["CCJ"]["effective_date"]
            == split_specifications["CCJ"]["effective_date"]
        )


class TestSplitShares:
    def test_should_split_shares(
        self, transactions, forward_split, split_specifications
    ):
        transactions = [
            transaction
            for transaction in transactions
            if transaction not in forward_split
        ]
        result = split_shares(transactions, split_specifications)
        result = next(filter(lambda x: x.symbol == "CCJ", result))

        assert result.quantity == Decimal("2.0")

    def test_should_divide_unit_price(
        self, transactions, forward_split, split_specifications
    ):
        transactions = [
            transaction
            for transaction in transactions
            if transaction not in forward_split
        ]
        result = split_shares(transactions, split_specifications)
        result = next(filter(lambda x: x.symbol == "CCJ", result))

        assert result.price == Decimal("20.19945")

    def test_should_not_change_symbol_after_effective_date(
        self, transactions, forward_split, split_specifications, trade_buy
    ):
        trade_buy.transaction_date = datetime.date(2023, 10, 1)
        transactions = [
            transaction
            for transaction in transactions
            if transaction not in forward_split
        ]
        transactions.append(trade_buy)

        result = split_shares(transactions, split_specifications)
        result = next(
            filter(
                lambda x: x.symbol == "CCJ"
                and x.transaction_date == datetime.date(2023, 10, 1),
                result,
            )
        )

        assert result == trade_buy

    def test_should_not_change_symbols_not_in_specifications(
        self,
        trade_buy,
        dividend_reinvestment_transaction_buy,
        split_specifications,
    ):
        transactions = [trade_buy, dividend_reinvestment_transaction_buy]

        result = split_shares(transactions, split_specifications)
        result = next(filter(lambda x: x.symbol == "KO", result))

        assert result == dividend_reinvestment_transaction_buy
