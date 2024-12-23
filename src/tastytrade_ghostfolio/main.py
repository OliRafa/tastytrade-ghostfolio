import datetime
from decimal import Decimal
from itertools import batched

from tastytrade import Account, ProductionSession
from tastytrade.account import Transaction

from tastytrade_ghostfolio.adapters.trade import adapt_trades
from tastytrade_ghostfolio.configs.settings import Settings
from tastytrade_ghostfolio.models.ghostfolio_account import GhostfolioAccount
from tastytrade_ghostfolio.models.ghostfolio_activity import GhostfolioActivity
from tastytrade_ghostfolio.repositories.symbol_mapping import (
    SymbolMappingRepository,
    SymbolMappingsNotFoundException,
)
from tastytrade_ghostfolio.services.ghostfolio import GhostfolioService


def get_tastytrade_session() -> ProductionSession:
    return ProductionSession(Settings.Tastytrade.USERNAME, Settings.Tastytrade.PASSWORD)


def get_tastytrade_account_history(session: ProductionSession) -> list[Transaction]:
    account = Account.get_accounts(session)[0]
    return account.get_history(session)


def filter_trades(transactions: list[Transaction]) -> list[Transaction]:
    trades = []
    for transaction in transactions:
        if transaction.transaction_type == "Trade" or (
            transaction.transaction_type == "Receive Deliver"
            and (
                transaction.transaction_sub_type == "Dividend"
                or transaction.transaction_sub_type == "Symbol Change"
                or transaction.transaction_sub_type == "Forward Split"
            )
        ):
            trades.append(transaction)

    return trades


def adapt_symbols(
    activities: list[Transaction] | list[GhostfolioActivity],
    symbol_mappings: dict[str, str],
) -> list[Transaction] | list[GhostfolioActivity]:
    for activity in activities:
        activity.symbol = symbol_mappings.get(activity.symbol, activity.symbol)

    return activities


def extract_symbol_changes(
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


def adapt_symbol_changes(
    transactions: list[Transaction], symbol_changes: list[Transaction]
) -> list[Transaction]:
    symbol_changes = sorted(symbol_changes, key=lambda x: x.transaction_date)

    symbol_changes_mapping = {}
    for changes in batched(symbol_changes, 2):
        old_symbol = next(filter(lambda x: x.action == "Sell to Close", changes))
        new_symbol = next(filter(lambda x: x.action == "Buy to Open", changes))
        symbol_changes_mapping[old_symbol.symbol] = new_symbol.symbol

    return adapt_symbols(transactions, symbol_changes_mapping)


def extract_forward_splits(
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


def get_split_specifications(
    splits: list[Transaction],
) -> tuple[list[Transaction], list[Transaction]]:
    splits = sorted(splits, key=lambda x: x.transaction_date)

    split_specifications = {}
    for split in batched(splits, 2):
        sell_transaction = next(filter(lambda x: x.action == "Sell to Close", split))
        buy_transaction = next(filter(lambda x: x.action == "Buy to Open", split))

        split_ratio = float(buy_transaction.quantity) / float(sell_transaction.quantity)

        split_specifications[buy_transaction.symbol] = {
            "effective_date": buy_transaction.transaction_date,
            "split_ratio": split_ratio,
        }

    return split_specifications


def split_shares(
    transactions: list[Transaction],
    split_specifications: dict[str, dict[str, int | datetime.date]],
) -> tuple[list[Transaction], list[Transaction]]:
    for transaction in transactions:
        if (
            transaction.symbol in split_specifications.keys()
            and transaction.transaction_date
            <= split_specifications[transaction.symbol]["effective_date"]
        ):
            transaction.quantity = transaction.quantity * Decimal(
                split_specifications[transaction.symbol]["split_ratio"]
            )

    return transactions


def extract_outdated_ghostfolio_orders(
    activities: list[GhostfolioActivity], orders: list[GhostfolioActivity]
) -> list[GhostfolioActivity]:
    outdated_orders: list[GhostfolioActivity] = []
    for order in orders:
        try:
            next(
                filter(
                    lambda x: x.date == order.date
                    and x.quantity == order.quantity
                    and x.symbol == order.symbol,
                    activities,
                )
            )
        except StopIteration:
            outdated_orders.append(order)

    return outdated_orders


def extract_activities_for_exporting(
    activities: list[GhostfolioActivity], orders: list[GhostfolioActivity]
) -> list[GhostfolioActivity]:
    activities_for_exporting: list[GhostfolioActivity] = []
    for activity in activities:
        try:
            next(
                filter(
                    lambda x: x.date == activity.date
                    and x.quantity == activity.quantity
                    and x.symbol == activity.symbol,
                    orders,
                )
            )
        except StopIteration:
            activities_for_exporting.append(activity)

    return activities_for_exporting


if __name__ == "__main__":
    ghostfolio_service = GhostfolioService()
    ghostfolio_accounts = ghostfolio_service.get_all_accounts()

    try:
        tastytrade_account = next(
            filter(
                lambda x: x.name.lower() in ["tastytrade", "tastyworks"],
                ghostfolio_accounts,
            )
        )

    except StopIteration:
        print("Creating new Tastytrade account in Ghostfolio...")
        tastytrade_account = GhostfolioAccount(name="Tastytrade")
        tastytrade_account = ghostfolio_service.create_account(tastytrade_account)

    session = get_tastytrade_session()
    print("Started getting all Tastytrade transactions...")
    transactions = get_tastytrade_account_history(session)

    trades = filter_trades(transactions)
    trades, symbol_changes = extract_symbol_changes(trades)
    if symbol_changes:
        print("Adapting symbol changes...")
        trades = adapt_symbol_changes(trades, symbol_changes)

    trades, forward_splits = extract_forward_splits(trades)
    if forward_splits:
        print("Adapting forward splits...")
        split_specifications = get_split_specifications(forward_splits)
        trades = split_shares(trades, split_specifications)

    activities = adapt_trades(trades)

    for activity in activities:
        activity.account_id = tastytrade_account.account_id
        activity.comment = "Activity created by Tastytrade-Ghostfolio."

    try:
        symbol_mappings = SymbolMappingRepository().get_symbol_mappings()
        activities = adapt_symbols(activities, symbol_mappings)
    except SymbolMappingsNotFoundException:
        print("Skipping symbol changes, as no mapping file was found.")

    print("Started exporting activities to Ghostfolio...")
    orders = ghostfolio_service.get_all_orders(tastytrade_account.account_id)
    outdated_orders = extract_outdated_ghostfolio_orders(activities, orders)
    if outdated_orders:
        print("Deleting outdated orders...")
        for order in outdated_orders:
            ghostfolio_service.delete_order(order)

    activities = extract_activities_for_exporting(activities, orders)
    if activities:
        print("Exporting new activities...")
        ghostfolio_service.export_activities_to_ghostfolio(activities)
    else:
        print("No new activities to import!")

    print("Done!")
