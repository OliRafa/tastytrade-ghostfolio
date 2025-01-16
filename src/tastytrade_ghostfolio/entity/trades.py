import datetime
from decimal import Decimal
from itertools import batched

from tastytrade.account import Transaction


class Trades:
    def __init__(self, transactions: list[Transaction]):
        self.transactions = transactions

    def adapt_symbol_changes(self) -> list[Transaction]:
        self.transactions, symbol_changes = self._extract_symbol_changes(
            self.transactions
        )
        if symbol_changes:
            print("Adapting symbol changes...")
            self.transactions = self._change_symbols(symbol_changes)

    @staticmethod
    def _extract_symbol_changes(
        transactions: list[Transaction],
    ) -> tuple[list[Transaction], list[Transaction]]:
        symbol_changes = [
            transaction
            for transaction in transactions
            if transaction.transaction_sub_type == "Symbol Change"
        ]

        if symbol_changes:
            for change in symbol_changes:
                transactions.remove(change)

        return transactions, symbol_changes

    def _change_symbols(self, symbol_changes: list[Transaction]) -> list[Transaction]:
        symbol_changes = sorted(symbol_changes, key=lambda x: x.transaction_date)

        symbol_changes_mapping = {}
        for changes in batched(symbol_changes, 2):
            old_symbol = next(filter(lambda x: x.action == "Sell to Close", changes))
            new_symbol = next(filter(lambda x: x.action == "Buy to Open", changes))
            symbol_changes_mapping[old_symbol.symbol] = new_symbol.symbol

        return self._adapt_symbols(self.transactions, symbol_changes_mapping)

    def _adapt_symbols(
        self, activities: list[Transaction], symbol_mappings: dict[str, str]
    ) -> list[Transaction]:
        for activity in activities:
            activity.symbol = symbol_mappings.get(activity.symbol, activity.symbol)

        return activities

    def adapt_split_shares(self):
        self.transactions, forward_splits = self._extract_forward_splits(
            self.transactions
        )
        if forward_splits:
            print("Adapting forward splits...")
            split_specifications = self._get_split_specifications(forward_splits)
            self.transactions = self._split_shares(
                self.transactions, split_specifications
            )

    @staticmethod
    def _extract_forward_splits(
        transactions: list[Transaction],
    ) -> tuple[list[Transaction], list[Transaction]]:
        symbol_changes = [
            transaction
            for transaction in transactions
            if transaction.transaction_sub_type == "Forward Split"
        ]

        if symbol_changes:
            for change in symbol_changes:
                transactions.remove(change)

        return transactions, symbol_changes

    @staticmethod
    def _get_split_specifications(
        splits: list[Transaction],
    ) -> tuple[list[Transaction], list[Transaction]]:
        splits = sorted(splits, key=lambda x: x.transaction_date)

        split_specifications = {}
        for split in batched(splits, 2):
            sell_transaction = next(
                filter(lambda x: x.action == "Sell to Close", split)
            )
            buy_transaction = next(filter(lambda x: x.action == "Buy to Open", split))

            split_ratio = float(buy_transaction.quantity) / float(
                sell_transaction.quantity
            )

            split_specifications[buy_transaction.symbol] = {
                "effective_date": buy_transaction.transaction_date,
                "split_ratio": split_ratio,
            }

        return split_specifications

    @staticmethod
    def _split_shares(
        transactions: list[Transaction],
        split_specifications: dict[str, dict[str, int | datetime.date]],
    ) -> tuple[list[Transaction], list[Transaction]]:
        for transaction in transactions:
            if (
                transaction.symbol in split_specifications.keys()
                and transaction.transaction_date
                <= split_specifications[transaction.symbol]["effective_date"]
            ):
                split_ratio = Decimal(
                    split_specifications[transaction.symbol]["split_ratio"]
                )
                transaction.quantity = transaction.quantity * split_ratio
                transaction.price = transaction.price / split_ratio

        return transactions
