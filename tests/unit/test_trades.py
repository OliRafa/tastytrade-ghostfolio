import datetime
from decimal import Decimal

from tastytrade_ghostfolio.entity.trades import Trades


class TestAdaptSymbolChanges:
    def test_should_map_old_symbol_to_new_one(self, transactions):
        trades = Trades(transactions)
        trades.adapt_symbol_changes()

        assert all(
            transaction.symbol == "COLA"
            for transaction in trades.transactions
            if transaction.transaction_sub_type == "Dividend"
        )


class TestExtractSymbolChanges:
    def test_when_theres_symbol_change_should_return_transactions_and_changes_separately(
        self, transactions, symbol_changeless_transactions, symbol_change
    ):
        clean_transactions, symbol_changes = Trades._extract_symbol_changes(
            transactions
        )

        assert clean_transactions == symbol_changeless_transactions
        assert symbol_changes == symbol_change

    def test_when_theres_no_symbol_change_should_return_all_transactions_and_empty_list(
        self, symbol_changeless_transactions
    ):
        clean_transactions, symbol_changes = Trades._extract_symbol_changes(
            symbol_changeless_transactions
        )

        assert clean_transactions == symbol_changeless_transactions
        assert symbol_changes == []


class TestExtractForwardSplits:
    def test_when_theres_forward_splits_should_return_transactions_and_splits_separately(
        self, transactions, forward_split
    ):
        clean_transactions, forward_splits = Trades._extract_forward_splits(
            transactions
        )

        assert forward_splits == forward_split
        assert forward_split not in clean_transactions


class TestGetSplitSpecifications:
    def test_should_return_effective_date_and_split_ratio(
        self, forward_split, split_specifications
    ):
        result = Trades._get_split_specifications(forward_split)

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
        result = Trades._split_shares(transactions, split_specifications)
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
        result = Trades._split_shares(transactions, split_specifications)
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

        result = Trades._split_shares(transactions, split_specifications)
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

        result = Trades._split_shares(transactions, split_specifications)
        result = next(filter(lambda x: x.symbol == "KO", result))

        assert result == dividend_reinvestment_transaction_buy
