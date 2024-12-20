import datetime
from decimal import Decimal

from pytest import fixture
from tastytrade.account import InstrumentType, PriceEffect, Transaction


@fixture
def trade_buy() -> Transaction:
    return Transaction.parse_obj(
        {
            "id": 261794408,
            "account_number": "6VV78917",
            "transaction_type": "Trade",
            "transaction_sub_type": "Buy to Open",
            "description": "Bought 1 CCJ @ 40.40",
            "executed_at": datetime.datetime(
                2023, 9, 27, 18, 36, 20, 28000, tzinfo=datetime.timezone.utc
            ),
            "transaction_date": datetime.date(2023, 9, 27),
            "value": Decimal("40.399"),
            "value_effect": PriceEffect.DEBIT,
            "net_value": Decimal("40.4"),
            "net_value_effect": PriceEffect.DEBIT,
            "is_estimated_fee": True,
            "symbol": "CCJ",
            "instrument_type": InstrumentType.EQUITY,
            "underlying_symbol": "CCJ",
            "action": "Buy to Open",
            "quantity": Decimal("1.0"),
            "price": Decimal("40.3989"),
            "regulatory_fees": Decimal("0.0"),
            "regulatory_fees_effect": PriceEffect.NONE,
            "clearing_fees": Decimal("0.001"),
            "clearing_fees_effect": PriceEffect.DEBIT,
            "commission": Decimal("0.0"),
            "commission_effect": PriceEffect.NONE,
            "proprietary_index_option_fees": Decimal("0.0"),
            "proprietary_index_option_fees_effect": PriceEffect.NONE,
            "ext_exchange_order_number": "38856857292356",
            "ext_global_order_number": 9047,
            "ext_group_id": "0",
            "ext_group_fill_id": "1251225",
            "ext_exec_id": "265753",
            "exec_id": "23_1251225265753",
            "exchange": "CDE",
            "order_id": 288165444,
            "exchange_affiliation_identifier": "",
            "leg_count": 1,
            "destination_venue": "CITADEL_EQUITIES_B",
            "other_charge": None,
            "other_charge_effect": None,
            "other_charge_description": None,
            "reverses_id": None,
            "cost_basis_reconciliation_date": None,
            "lots": None,
            "agency_price": None,
            "principal_price": None,
        }
    )


@fixture
def dividends() -> list[Transaction]:
    return [
        Transaction.parse_obj(
            {
                "account_number": "6VV78917",
                "action": None,
                "agency_price": None,
                "clearing_fees": None,
                "clearing_fees_effect": None,
                "commission": None,
                "commission_effect": None,
                "cost_basis_reconciliation_date": None,
                "description": "COCA COLA COMPANY",
                "destination_venue": None,
                "exchange": None,
                "exchange_affiliation_identifier": None,
                "exec_id": None,
                "executed_at": datetime.datetime(
                    2023, 12, 15, 22, 0, tzinfo=datetime.timezone.utc
                ),
                "ext_exchange_order_number": None,
                "ext_exec_id": None,
                "ext_global_order_number": None,
                "ext_group_fill_id": None,
                "ext_group_id": None,
                "id": 274072375,
                "instrument_type": InstrumentType.EQUITY,
                "is_estimated_fee": True,
                "leg_count": None,
                "lots": None,
                "net_value": Decimal("0.96"),
                "net_value_effect": PriceEffect.CREDIT,
                "order_id": None,
                "other_charge": None,
                "other_charge_description": None,
                "other_charge_effect": None,
                "price": None,
                "principal_price": None,
                "proprietary_index_option_fees": None,
                "proprietary_index_option_fees_effect": None,
                "quantity": None,
                "regulatory_fees": None,
                "regulatory_fees_effect": None,
                "reverses_id": None,
                "symbol": "KO",
                "transaction_date": datetime.date(2023, 12, 15),
                "transaction_sub_type": "Dividend",
                "transaction_type": "Money Movement",
                "underlying_symbol": "KO",
                "value": Decimal("0.96"),
                "value_effect": PriceEffect.CREDIT,
            }
        ),
        Transaction.parse_obj(
            {
                "account_number": "6VV78917",
                "action": None,
                "agency_price": None,
                "clearing_fees": None,
                "clearing_fees_effect": None,
                "commission": None,
                "commission_effect": None,
                "cost_basis_reconciliation_date": None,
                "description": "COCA COLA COMPANY",
                "destination_venue": None,
                "exchange": None,
                "exchange_affiliation_identifier": None,
                "exec_id": None,
                "executed_at": datetime.datetime(
                    2023, 12, 15, 22, 0, tzinfo=datetime.timezone.utc
                ),
                "ext_exchange_order_number": None,
                "ext_exec_id": None,
                "ext_global_order_number": None,
                "ext_group_fill_id": None,
                "ext_group_id": None,
                "id": 274072373,
                "instrument_type": InstrumentType.EQUITY,
                "is_estimated_fee": True,
                "leg_count": None,
                "lots": None,
                "net_value": Decimal("0.14"),
                "net_value_effect": PriceEffect.DEBIT,
                "order_id": None,
                "other_charge": None,
                "other_charge_description": None,
                "other_charge_effect": None,
                "price": None,
                "principal_price": None,
                "proprietary_index_option_fees": None,
                "proprietary_index_option_fees_effect": None,
                "quantity": None,
                "regulatory_fees": None,
                "regulatory_fees_effect": None,
                "reverses_id": None,
                "symbol": "KO",
                "transaction_date": datetime.date(2023, 12, 15),
                "transaction_sub_type": "Dividend",
                "transaction_type": "Money Movement",
                "underlying_symbol": "KO",
                "value": Decimal("0.14"),
                "value_effect": PriceEffect.DEBIT,
            }
        ),
    ]


@fixture
def dividend_reinvestment_transaction_buy() -> list[Transaction]:
    return Transaction.parse_obj(
        {
            "account_number": "6VV78917",
            "action": "Buy to Open",
            "agency_price": None,
            "clearing_fees": None,
            "clearing_fees_effect": None,
            "commission": None,
            "commission_effect": None,
            "cost_basis_reconciliation_date": None,
            "description": "Received 0.01391 Long KO via Dividend",
            "destination_venue": None,
            "exchange": None,
            "exchange_affiliation_identifier": None,
            "exec_id": None,
            "executed_at": datetime.datetime(
                2023, 12, 15, 22, 0, tzinfo=datetime.timezone.utc
            ),
            "ext_exchange_order_number": None,
            "ext_exec_id": None,
            "ext_global_order_number": None,
            "ext_group_fill_id": None,
            "ext_group_id": None,
            "id": 274083974,
            "instrument_type": InstrumentType.EQUITY,
            "is_estimated_fee": True,
            "leg_count": None,
            "lots": None,
            "net_value": Decimal("0.0"),
            "net_value_effect": PriceEffect.NONE,
            "order_id": None,
            "other_charge": None,
            "other_charge_description": None,
            "other_charge_effect": None,
            "price": Decimal("59.04"),
            "principal_price": None,
            "proprietary_index_option_fees": None,
            "proprietary_index_option_fees_effect": None,
            "quantity": Decimal("0.01391"),
            "regulatory_fees": None,
            "regulatory_fees_effect": None,
            "reverses_id": None,
            "symbol": "KO",
            "transaction_date": datetime.date(2023, 12, 15),
            "transaction_sub_type": "Dividend",
            "transaction_type": "Receive Deliver",
            "underlying_symbol": "KO",
            "value": Decimal("0.0"),
            "value_effect": PriceEffect.NONE,
        }
    )


@fixture
def divident_reinvestment(dividend_reinvestment_transaction_buy) -> list[Transaction]:
    return [
        dividend_reinvestment_transaction_buy,
        Transaction.parse_obj(
            {
                "account_number": "6VV78917",
                "action": None,
                "agency_price": None,
                "clearing_fees": None,
                "clearing_fees_effect": None,
                "commission": None,
                "commission_effect": None,
                "cost_basis_reconciliation_date": None,
                "description": "Cash dividend reinvested info KO",
                "destination_venue": None,
                "exchange": None,
                "exchange_affiliation_identifier": None,
                "exec_id": None,
                "executed_at": datetime.datetime(
                    2023, 12, 15, 22, 0, tzinfo=datetime.timezone.utc
                ),
                "ext_exchange_order_number": None,
                "ext_exec_id": None,
                "ext_global_order_number": None,
                "ext_group_fill_id": None,
                "ext_group_id": None,
                "id": 274072371,
                "instrument_type": InstrumentType.EQUITY,
                "is_estimated_fee": True,
                "leg_count": None,
                "lots": None,
                "net_value": Decimal("0.82"),
                "net_value_effect": PriceEffect.DEBIT,
                "order_id": None,
                "other_charge": None,
                "other_charge_description": None,
                "other_charge_effect": None,
                "price": None,
                "principal_price": None,
                "proprietary_index_option_fees": None,
                "proprietary_index_option_fees_effect": None,
                "quantity": None,
                "regulatory_fees": None,
                "regulatory_fees_effect": None,
                "reverses_id": None,
                "symbol": "KO",
                "transaction_date": datetime.date(2023, 12, 15),
                "transaction_sub_type": "Withdrawal",
                "transaction_type": "Money Movement",
                "underlying_symbol": "KO",
                "value": Decimal("0.82"),
                "value_effect": PriceEffect.DEBIT,
            }
        ),
    ]


@fixture
def symbol_change_sell_old() -> Transaction:
    return Transaction.parse_obj(
        {
            "account_number": "6VV78917",
            "action": "Sell to Close",
            "agency_price": None,
            "clearing_fees": None,
            "clearing_fees_effect": None,
            "commission": None,
            "commission_effect": None,
            "cost_basis_reconciliation_date": None,
            "description": "Symbol change:  Close 5.47124 EURN",
            "destination_venue": None,
            "exchange": None,
            "exchange_affiliation_identifier": None,
            "exec_id": None,
            "executed_at": datetime.datetime(
                2024, 7, 15, 10, 0, tzinfo=datetime.timezone.utc
            ),
            "ext_exchange_order_number": None,
            "ext_exec_id": None,
            "ext_global_order_number": None,
            "ext_group_fill_id": None,
            "ext_group_id": None,
            "id": 820695443,
            "instrument_type": InstrumentType.EQUITY,
            "is_estimated_fee": True,
            "leg_count": None,
            "lots": None,
            "net_value": Decimal("82.165"),
            "net_value_effect": PriceEffect.CREDIT,
            "order_id": None,
            "other_charge": None,
            "other_charge_description": None,
            "other_charge_effect": None,
            "price": None,
            "principal_price": None,
            "proprietary_index_option_fees": None,
            "proprietary_index_option_fees_effect": None,
            "quantity": Decimal("5.47124"),
            "regulatory_fees": None,
            "regulatory_fees_effect": None,
            "reverses_id": None,
            "symbol": "EURN",
            "transaction_date": datetime.date(2024, 7, 15),
            "transaction_sub_type": "Symbol Change",
            "transaction_type": "Receive Deliver",
            "underlying_symbol": "EURN",
            "value": Decimal("82.165"),
            "value_effect": PriceEffect.CREDIT,
        }
    )


@fixture
def symbol_change_buy_new() -> Transaction:
    return Transaction.parse_obj(
        {
            "account_number": "6VV78917",
            "action": "Buy to Open",
            "agency_price": None,
            "clearing_fees": None,
            "clearing_fees_effect": None,
            "commission": None,
            "commission_effect": None,
            "cost_basis_reconciliation_date": None,
            "description": "Symbol change:  Open 5.47124 CMBT",
            "destination_venue": None,
            "exchange": None,
            "exchange_affiliation_identifier": None,
            "exec_id": None,
            "executed_at": datetime.datetime(
                2024, 7, 15, 10, 0, tzinfo=datetime.timezone.utc
            ),
            "ext_exchange_order_number": None,
            "ext_exec_id": None,
            "ext_global_order_number": None,
            "ext_group_fill_id": None,
            "ext_group_id": None,
            "id": 820695444,
            "instrument_type": InstrumentType.EQUITY,
            "is_estimated_fee": True,
            "leg_count": None,
            "lots": None,
            "net_value": Decimal("82.165"),
            "net_value_effect": PriceEffect.DEBIT,
            "order_id": None,
            "other_charge": None,
            "other_charge_description": None,
            "other_charge_effect": None,
            "price": None,
            "principal_price": None,
            "proprietary_index_option_fees": None,
            "proprietary_index_option_fees_effect": None,
            "quantity": Decimal("5.47124"),
            "regulatory_fees": None,
            "regulatory_fees_effect": None,
            "reverses_id": None,
            "symbol": "CMBT",
            "transaction_date": datetime.date(2024, 7, 15),
            "transaction_sub_type": "Symbol Change",
            "transaction_type": "Receive Deliver",
            "underlying_symbol": "CMBT",
            "value": Decimal("82.165"),
            "value_effect": PriceEffect.DEBIT,
        }
    )


@fixture
def symbol_change(symbol_change_sell_old, symbol_change_buy_new) -> list[Transaction]:
    return [symbol_change_sell_old, symbol_change_buy_new]


@fixture
def transactions(
    dividends, divident_reinvestment, trade_buy, symbol_change
) -> list[Transaction]:
    return [*dividends, *divident_reinvestment, trade_buy, *symbol_change]
