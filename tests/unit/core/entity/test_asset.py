import datetime
from decimal import Decimal

from pytest import fixture

from tastytrade_ghostfolio.core.entity.asset import Asset
from tastytrade_ghostfolio.core.entity.split import Split
from tastytrade_ghostfolio.core.entity.trade import Trade
from tastytrade_ghostfolio.core.entity.transaction_type import TransactionType
from tests.conftest import mark_test


class AssetFactory:
    @fixture
    def trade(self) -> Trade:
        return Trade(
            executed_at=datetime.datetime(
                2023, 9, 27, 18, 36, 20, 28000, tzinfo=datetime.timezone.utc
            ),
            fee=Decimal("0.001"),
            quantity=Decimal("1.0"),
            symbol="STOCKA",
            transaction_type=TransactionType.BUY,
            unit_price=Decimal("40.3989"),
        )

    @fixture(autouse=True)
    def asset(self, trade):
        self.asset: Asset = Asset(symbol="STOCKA")
        self.asset.add_trades([trade])


class TestSplitShares(AssetFactory):
    @fixture
    def split(self) -> Split:
        return Split(
            effective_date=datetime.datetime(2023, 9, 28), ratio=2, symbol="CCJ"
        )

    @mark_test
    def should_split_before_effective_date(self, split):
        self.asset.split_shares(split)

        assert self.asset.trades[0].quantity == Decimal("2.0")

    @mark_test
    def test_should_divide_unit_price(self, split):
        self.asset.split_shares(split)

        assert self.asset.trades[0].unit_price == Decimal("20.19945")

    @mark_test
    def test_should_not_change_symbol_after_effective_date(self, split):
        after_the_fact_trade = self.asset.trades[0].model_copy()
        after_the_fact_trade.executed_at = datetime.datetime(
            2023, 10, 1, tzinfo=datetime.timezone.utc
        )
        self.asset.add_trades([after_the_fact_trade.model_copy()])

        self.asset.split_shares(split)

        assert self.asset.trades[1] == after_the_fact_trade


class TestHasTrade(AssetFactory):
    @mark_test
    def should_return_true_when_trade_exists(self, trade):
        result = self.asset.has_trade(trade)

        assert result is True

    @mark_test
    def should_return_false_when_trade_doesnt_exist(self):
        trade = Trade(
            executed_at=datetime.datetime(
                2023, 9, 30, 18, 36, 20, 28000, tzinfo=datetime.timezone.utc
            ),
            fee=Decimal("0.001"),
            quantity=Decimal("1.0"),
            symbol="STOCKA",
            transaction_type=TransactionType.BUY,
            unit_price=Decimal("40.3989"),
        )

        result = self.asset.has_trade(trade)

        assert result is False


class TestGetTrade(AssetFactory):
    @mark_test
    def should_return_trade(self, trade: Trade):
        result = self.asset.get_trade(
            trade.executed_at, trade.quantity, trade.symbol, trade.unit_price
        )

        assert result == trade


class TestDeleteTrade(AssetFactory):
    @mark_test
    def should_delete_trade(self, trade):
        self.asset.delete_trade(trade)

        results = self.asset.trades

        assert not results


class TestChangeSymbol(AssetFactory):
    @mark_test
    def should_change_asset_symbol(self):
        self.asset.change_symbol("NEWSTOCKA")

        assert self.asset.symbol == "NEWSTOCKA"

    @mark_test
    def should_change_symbol_for_all_trades(self):
        self.asset.change_symbol("NEWSTOCKA")

        results = self.asset.trades

        assert all(trade.symbol == "NEWSTOCKA" for trade in results)
