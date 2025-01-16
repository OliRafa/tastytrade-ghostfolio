from tastytrade_ghostfolio.adapters.trade import adapt_trades
from tastytrade_ghostfolio.entity.ghostfolio_trades import GhostfolioTrades
from tastytrade_ghostfolio.entity.trades import Trades
from tastytrade_ghostfolio.models.ghostfolio_account import GhostfolioAccount
from tastytrade_ghostfolio.models.ghostfolio_activity import GhostfolioActivity
from tastytrade_ghostfolio.repositories.symbol_mapping import (
    SymbolMappingRepository,
    SymbolMappingsNotFoundException,
)
from tastytrade_ghostfolio.services.ghostfolio import GhostfolioService
from tastytrade_ghostfolio.services.tastytrade import TastytradeService


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
                    and x.symbol == order.symbol
                    and x.unit_price == order.unit_price,
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
                    and x.symbol == activity.symbol
                    and x.unit_price == activity.unit_price,
                    orders,
                )
            )
        except StopIteration:
            activities_for_exporting.append(activity)

    return activities_for_exporting


if __name__ == "__main__":
    ghostfolio_service = GhostfolioService()
    tastytrade_account = ghostfolio_service.get_or_create_account()

    tastytrade_service = TastytradeService()
    print("Started getting all Tastytrade transactions...")
    transactions = tastytrade_service.get_trades_history()

    trades = Trades(transactions)
    trades.adapt_symbol_changes()
    trades.adapt_split_shares()

    ghostfolio_trades = GhostfolioTrades(adapt_trades(trades.transactions))
    ghostfolio_trades.add_account_info(tastytrade_account.account_id)

    try:
        symbol_mappings = SymbolMappingRepository().get_symbol_mappings()
        activities = ghostfolio_trades.adapt_symbols(symbol_mappings)
    except SymbolMappingsNotFoundException:
        print("Skipping symbol changes, as no mapping file was found.")

    print("Started exporting activities to Ghostfolio...")
    orders = ghostfolio_service.get_all_orders(tastytrade_account.account_id)
    outdated_orders = extract_outdated_ghostfolio_orders(
        ghostfolio_trades.activities, orders
    )
    if outdated_orders:
        print("Deleting outdated orders...")
        for order in outdated_orders:
            ghostfolio_service.delete_order(order)

    activities = extract_activities_for_exporting(ghostfolio_trades.activities, orders)
    if activities:
        print("Exporting new activities...")
        ghostfolio_service.export_activities_to_ghostfolio(activities)
    else:
        print("No new activities to import!")

    print("Done!")
