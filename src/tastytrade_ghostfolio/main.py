from itertools import batched

from tastytrade import Account, ProductionSession
from tastytrade.account import Transaction

from tastytrade_ghostfolio.adapters.trade import adapt_trades
from tastytrade_ghostfolio.configs.settings import Settings
from tastytrade_ghostfolio.models.ghostfolio_account import GhostfolioAccount
from tastytrade_ghostfolio.models.ghostfolio_activity import (
    GhostfolioActivity,
    TransactionType,
)
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

    activities = adapt_trades(trades)

    for activity in activities:
        activity.account_id = tastytrade_account.account_id
        activity.comment = "Activity created by Tastytrade-Ghostfolio."

    orders = ghostfolio_service.get_all_orders(tastytrade_account.account_id)

    print("Started exporting activities to Ghostfolio...")
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

    try:
        symbol_mappings = SymbolMappingRepository().get_symbol_mappings()
        activities_for_exporting = adapt_symbols(
            activities_for_exporting, symbol_mappings
        )
    except SymbolMappingsNotFoundException:
        print("Skipping symbol changes, as no mapping file was found.")

    ghostfolio_service.export_activities_to_ghostfolio(activities_for_exporting)
    print("Done!")
