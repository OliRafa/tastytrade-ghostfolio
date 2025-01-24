from tastytrade_ghostfolio.core.entity.portfolio import Portfolio
from tastytrade_ghostfolio.infra.ghostfolio.ghostfolio_adapter import GhostfolioAdapter
from tastytrade_ghostfolio.infra.ghostfolio.ghostfolio_api import GhostfolioApi
from tastytrade_ghostfolio.infra.tastytrade.tastytrade_adapter import TastytradeAdapter
from tastytrade_ghostfolio.infra.tastytrade.tastytrade_api import TastytradeApi
from tastytrade_ghostfolio.repositories.symbol_mapping import (
    SymbolMappingRepository,
    SymbolMappingsNotFoundException,
)

if __name__ == "__main__":
    print("Started getting all Tastytrade transactions...")
    tastytrade = TastytradeAdapter(TastytradeApi())

    portfolio = Portfolio()
    symbols = tastytrade.get_assets()
    for symbol in symbols:
        trades = tastytrade.get_trades(symbol)
        portfolio.add_asset(symbol, trades)
        dividend_reinvestments = tastytrade.get_dividends(symbol)
        if dividend_reinvestments:
            portfolio.add_dividends(symbol, dividend_reinvestments)

    ghostfolio = GhostfolioAdapter(GhostfolioApi())
    ghostfolio_account = ghostfolio.get_or_create_account()
    ghostfolio_account.add_portfolio(portfolio)

    symbol_changes = tastytrade.get_symbol_changes()
    if symbol_changes:
        print("Adapting symbol changes...")
        portfolio.adapt_symbol_changes(symbol_changes)

        for change in symbol_changes:
            outdated_orders = ghostfolio.get_orders_by_symbol(
                ghostfolio_account.account_id, change.old_symbol
            )
            if outdated_orders:
                print(
                    f'Deleting outdated orders for "{change.old_symbol}" '
                    f'after changing to "{change.new}"...'
                )
                ghostfolio.delete_orders(outdated_orders)

    stock_splits = tastytrade.get_splits()
    if stock_splits:
        print("Handling stock splits...")
        portfolio.adapt_stock_splits(stock_splits)

    try:
        symbol_mappings = SymbolMappingRepository().get_symbol_mappings()
        print("Handling symbol changes from mapping file...")
        portfolio.adapt_symbol_changes(symbol_mappings)

    except SymbolMappingsNotFoundException:
        print("Skipping symbol changes, as no mapping file was found.")

    print("Started exporting activities to Ghostfolio...")
    symbols = portfolio.get_symbols()
    for symbol in symbols:
        orders = ghostfolio.get_orders_by_symbol(ghostfolio_account.account_id, symbol)

        outdated_orders = portfolio.get_absent_trades(symbol, orders)
        if outdated_orders:
            print(f"Deleting outdated orders for `{symbol}`...")
            ghostfolio.delete_orders(outdated_orders)
            orders = [order for order in orders if order not in outdated_orders]

        if orders:
            portfolio.delete_repeated_trades(symbol, orders)

    print("Exporting new activities to Ghostfolio...")
    ghostfolio.export_portfolio(ghostfolio_account)

    # if activities:
    #     ghostfolio_service.export_activities_to_ghostfolio(activities)
    # else:
    #     print("No new activities to import!")

    print("Done!")
