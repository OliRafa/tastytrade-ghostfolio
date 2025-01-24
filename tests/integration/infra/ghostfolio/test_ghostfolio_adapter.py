from pytest import fixture

from tastytrade_ghostfolio.core.entity.account import GhostfolioAccount
from tastytrade_ghostfolio.core.entity.portfolio import Portfolio
from tastytrade_ghostfolio.infra.ghostfolio.ghostfolio_adapter import GhostfolioAdapter
from tests.conftest import mark_test
from tests.infra.ghostfolio_api import InMemoryGhostfolioApi


@fixture
def account_id() -> str:
    return "2a7efb1f-8f3c-43de-8778-f8488f1719d3"


@fixture
def account(account_id, stock_a_trades, stock_b_trades) -> GhostfolioAccount:
    portfolio = Portfolio()
    portfolio.add_asset("STOCKA", stock_a_trades)
    portfolio.add_asset("STOCKB", stock_b_trades)

    account = GhostfolioAccount(account_id=account_id, name="Tastytrade")
    account.add_portfolio(portfolio)

    return account


class GhostfolioAdapterFactory:
    @fixture(autouse=True)
    def ghostfolio_adapter(self):
        self.ghostfolio_adapter: GhostfolioAdapter = GhostfolioAdapter(
            InMemoryGhostfolioApi()
        )


class TestGetOrCreateAccount(GhostfolioAdapterFactory):
    @mark_test
    def should_create_if_not_exist(self):
        result = self.ghostfolio_adapter.get_or_create_account()

        assert result.name == "Tastytrade"


class TestGetOrdersBySymbol(GhostfolioAdapterFactory):
    @mark_test
    def should_return_only_orders_for_given_symbol(self, account_id):
        results = self.ghostfolio_adapter.get_orders_by_symbol(account_id, "STOCKA")

        assert all(result.symbol == "STOCKA" for result in results)

    @mark_test
    def when_orders_are_absent_should_return_empty_list(self, account_id):
        results = self.ghostfolio_adapter.get_orders_by_symbol(account_id, "NOTASTOCK")

        assert not results


class TestDeleteOrders(GhostfolioAdapterFactory):
    @mark_test
    def should_delete_orders(self, account_id):
        orders = self.ghostfolio_adapter.get_orders_by_symbol(account_id, "STOCKA")

        self.ghostfolio_adapter.delete_orders(orders)

        orders = self.ghostfolio_adapter.get_orders_by_symbol(account_id, "STOCKA")
        assert not orders


class TestExportPortfolio(GhostfolioAdapterFactory):
    @mark_test
    def should_export_all_trades_in_portfolio(
        self, account, stock_a_trades, stock_b_trades
    ):
        orders = self.ghostfolio_adapter.get_orders_by_symbol(
            account.account_id, "STOCKA"
        )
        self.ghostfolio_adapter.delete_orders(orders)
        orders = self.ghostfolio_adapter.get_orders_by_symbol(
            account.account_id, "STOCKB"
        )
        self.ghostfolio_adapter.delete_orders(orders)

        self.ghostfolio_adapter.export_portfolio(account)

        result = self.ghostfolio_adapter.get_orders_by_symbol(
            account.account_id, "STOCKA"
        )

        assert len(result) == len(stock_a_trades)

        result = self.ghostfolio_adapter.get_orders_by_symbol(
            account.account_id, "STOCKB"
        )

        assert len(result) == len(stock_b_trades)
