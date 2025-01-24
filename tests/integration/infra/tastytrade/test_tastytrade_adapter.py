import datetime
from decimal import Decimal

from pytest import fixture
from tastytrade.account import Transaction

from tastytrade_ghostfolio.infra.tastytrade.tastytrade_adapter import TastytradeAdapter
from tests.conftest import mark_test
from tests.infra.tastytrade_api import InMemoryTastytradeApi


class TastytradeAdapterFactory:
    @fixture(autouse=True, scope="function")
    def tastytrade_adapter(self) -> TastytradeAdapter:
        self.tastytrade_adapter = TastytradeAdapter(InMemoryTastytradeApi())


class TestTotalFee(TastytradeAdapterFactory):
    @mark_test
    def should_return_a_positive_number(self):
        result = TastytradeAdapter._calculate_total_fee(
            Decimal("-0.001"), Decimal("-0.4"), Decimal("-0.03"), Decimal("0.0")
        )
        assert result == Decimal("0.431")

    @mark_test
    def should_aggregate_fees(self):
        result = TastytradeAdapter._calculate_total_fee(
            Decimal("-0.001"), Decimal("0.0"), Decimal("0.0"), Decimal("0.0")
        )
        assert result > Decimal("0.0")

    @mark_test
    def when_any_fee_isnt_given_should_assume_zero(self):
        result = TastytradeAdapter._calculate_total_fee(None, None, None, None)
        assert result == Decimal("0.0")


class TestGetTrades(TastytradeAdapterFactory):
    @mark_test
    def when_given_asset_should_return_trades_for_requested_asset_only(self):
        results = self.tastytrade_adapter.get_trades("STOCKA")

        assert len(results) == 1
        assert results[0].symbol == "STOCKA"

    @mark_test
    def when_no_asset_is_given_should_return_all_trades(self):
        results = self.tastytrade_adapter.get_trades()

        assert len(results) == 3
        assert any(trade.symbol == "STOCKA" for trade in results)
        assert any(trade.symbol == "STOCKB" for trade in results)
        assert any(trade.symbol == "STOCKBB" for trade in results)


class TestGetAssets(TastytradeAdapterFactory):
    @mark_test
    def should_return_all_assets(self):
        results = self.tastytrade_adapter.get_assets()

        assert len(results) == 3

    @mark_test
    def when_theres_aditional_history_entries_should_return_only_existing_assets(self):
        self.tastytrade_adapter._history.append(
            Transaction(
                id=1,
                account_number="",
                transaction_type="Another",
                transaction_sub_type="Another Sub Type",
                description="",
                executed_at=datetime.datetime.now(),
                transaction_date=datetime.date.today(),
                value=Decimal("0.0"),
                net_value=Decimal("0.0"),
                is_estimated_fee=True,
                symbol=None,
            )
        )
        results = self.tastytrade_adapter.get_assets()

        assert all(asset is not None for asset in results)

    @mark_test
    def when_after_symbol_change_theres_no_new_trade_should_add_dividends(self):
        self.tastytrade_adapter = TastytradeAdapter(InMemoryTastytradeApi())
        self.tastytrade_adapter._history.append(
            Transaction(
                id=1,
                action="Buy to Open",
                account_number="",
                transaction_type="Receive Deliver",
                transaction_sub_type="Dividend",
                description="",
                executed_at=datetime.datetime.now(),
                transaction_date=datetime.date.today(),
                value=Decimal("0.0"),
                net_value=Decimal("0.0"),
                is_estimated_fee=True,
                symbol="STOCKC",
                quantity=Decimal("0.1"),
                price=Decimal("10.0"),
            )
        )
        results = self.tastytrade_adapter.get_assets()

        assert "STOCKC" in results


class TestGetSymbolChanges(TastytradeAdapterFactory):
    @mark_test
    def should_return_all_symbol_changes(self):
        results = self.tastytrade_adapter.get_symbol_changes()

        assert len(results) == 1
        assert results[0].old_symbol == "STOCKB"
        assert results[0].new_symbol == "STOCKBB"


class TestGetSplits(TastytradeAdapterFactory):
    @mark_test
    def should_return_all_forward_splits(self):
        results = self.tastytrade_adapter.get_splits()

        assert len(results) == 1
        assert results[0].symbol == "STOCKA"
        assert results[0].ratio == Decimal("2.0")
        assert results[0].effective_date == datetime.date(2023, 9, 28)


class TestGetDividends(TastytradeAdapterFactory):
    @mark_test
    def should_return_dividend_reinvestments(self):
        results = self.tastytrade_adapter.get_dividends("STOCKB")

        assert len(results) == 1
        assert results[0].symbol == "STOCKB"
        assert results[0].quantity == Decimal("0.01391")
