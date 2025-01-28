from tastytrade_ghostfolio.core.entity.portfolio import Portfolio
from tastytrade_ghostfolio.infra.dividends_provider.dividends_provider_adapter import (
    DividendsProviderAdapter,
)
from tastytrade_ghostfolio.infra.dividends_provider.yahoo_finance_api import (
    YahooFinanceApi,
)
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
    dividends_provider = DividendsProviderAdapter(YahooFinanceApi())

    ghostfolio = GhostfolioAdapter(GhostfolioApi())
    ghostfolio_account = ghostfolio.get_or_create_account()

    portfolio = Portfolio()
    symbol_changes = tastytrade.get_symbol_changes()
    if symbol_changes:
        print("Adapting symbol changes...")
        for change in symbol_changes:
            trades = tastytrade.get_trades(change.old_symbol)
            portfolio.add_asset(change.old_symbol, trades)

            trades = tastytrade.get_trades(change.new_symbol)
            portfolio.add_asset(change.new_symbol, trades)
            portfolio.adapt_symbol_changes(symbol_changes)

            old_dividends = tastytrade.get_dividends(change.old_symbol)
            new_dividends = tastytrade.get_dividends(change.new_symbol)
            if old_dividends or new_dividends:
                dividend_infos = dividends_provider.get_by_symbol(change.new_symbol)
                if old_dividends:
                    for dividend in old_dividends:
                        dividend.symbol = change.new_symbol

                portfolio.add_dividends(
                    change.new_symbol, old_dividends + new_dividends, dividend_infos
                )

            outdated_orders = ghostfolio.get_orders_by_symbol(
                ghostfolio_account.account_id, change.old_symbol
            )
            if outdated_orders:
                print(
                    f'Deleting outdated orders for "{change.old_symbol}" '
                    f'after changing to "{change.new}"...'
                )
                ghostfolio.delete_orders(outdated_orders)

    symbols = tastytrade.get_assets()
    symbols = [
        symbol
        for symbol in symbols
        if symbol not in portfolio.get_symbols() and symbol not in symbol_changes
    ]
    for symbol in symbols:
        trades = tastytrade.get_trades(symbol)
        portfolio.add_asset(symbol, trades)

        dividends = tastytrade.get_dividends(symbol)
        if dividends:
            dividend_infos = dividends_provider.get_by_symbol(symbol)
            portfolio.add_dividends(symbol, dividends, dividend_infos)

    stock_splits = tastytrade.get_splits()
    if stock_splits:
        print("Handling stock splits...")
        portfolio.adapt_stock_splits(stock_splits)

    try:
        symbol_mappings = SymbolMappingRepository().get_symbol_mappings()
        print("Handling symbol changes from mapping file...")
        portfolio.adapt_symbol_changes(symbol_mappings)

    except SymbolMappingsNotFoundException:
        print("Skipping symbol changes from mapping file, as no file was found.")

    print("Started exporting activities to Ghostfolio...")
    for symbol in portfolio.get_symbols():
        orders = ghostfolio.get_orders_by_symbol(ghostfolio_account.account_id, symbol)

        outdated_orders = portfolio.get_absent_trades(symbol, orders)
        if outdated_orders:
            print(f"Deleting outdated orders for `{symbol}`...")
            ghostfolio.delete_orders(outdated_orders)
            orders = [order for order in orders if order not in outdated_orders]

        if orders:
            portfolio.delete_repeated_trades(symbol, orders)

    print("Exporting new activities to Ghostfolio...")
    ghostfolio_account.add_portfolio(portfolio)
    ghostfolio.export_portfolio(ghostfolio_account)

    # if activities:
    #     ghostfolio_service.export_activities_to_ghostfolio(activities)
    # else:
    #     print("No new activities to import!")

    print("Done!")
