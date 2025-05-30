import datetime
from decimal import Decimal

from tastytrade.account import InstrumentType, Transaction

trade_buys = [
    Transaction(
        **{
            "id": 261794408,
            "account_number": "6VV78917",
            "transaction_type": "Trade",
            "transaction_sub_type": "Buy to Open",
            "description": "Bought 1 STOCKA @ 40.40",
            "executed_at": datetime.datetime(
                2023, 9, 27, 18, 36, 20, 28000, tzinfo=datetime.timezone.utc
            ),
            "transaction_date": datetime.date(2023, 9, 27),
            "value": Decimal("-40.399"),
            "net_value": Decimal("-40.4"),
            "is_estimated_fee": True,
            "symbol": "STOCKA",
            "instrument_type": InstrumentType.EQUITY,
            "underlying_symbol": "STOCKA",
            "action": "Buy to Open",
            "quantity": Decimal("1.0"),
            "price": Decimal("40.3989"),
            "regulatory_fees": Decimal("0.0"),
            "clearing_fees": Decimal("-0.001"),
            "commission": Decimal("0.0"),
            "proprietary_index_option_fees": Decimal("0.0"),
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
    ),
    Transaction(
        **{
            "id": 261794408,
            "account_number": "6VV78917",
            "transaction_type": "Trade",
            "transaction_sub_type": "Buy to Open",
            "description": "Bought 1 STOCKA @ 40.40",
            "executed_at": datetime.datetime(
                2023, 9, 27, 18, 36, 20, 28000, tzinfo=datetime.timezone.utc
            ),
            "transaction_date": datetime.date(2023, 9, 27),
            "value": Decimal("-40.399"),
            "net_value": Decimal("-40.4"),
            "is_estimated_fee": True,
            "symbol": "STOCKB",
            "instrument_type": InstrumentType.EQUITY,
            "underlying_symbol": "STOCKB",
            "action": "Buy to Open",
            "quantity": Decimal("1.0"),
            "price": Decimal("40.3989"),
            "regulatory_fees": Decimal("0.0"),
            "clearing_fees": Decimal("-0.001"),
            "commission": Decimal("0.0"),
            "proprietary_index_option_fees": Decimal("0.0"),
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
    ),
    Transaction(
        **{
            "id": 261794408,
            "account_number": "6VV78917",
            "transaction_type": "Trade",
            "transaction_sub_type": "Buy to Open",
            "description": "Bought 1 STOCKA @ 40.40",
            "executed_at": datetime.datetime(
                2024, 7, 20, 10, 0, tzinfo=datetime.timezone.utc
            ),
            "transaction_date": datetime.date(2024, 7, 20),
            "value": Decimal("-40.399"),
            "net_value": Decimal("-40.4"),
            "is_estimated_fee": True,
            "symbol": "STOCKBB",
            "instrument_type": InstrumentType.EQUITY,
            "underlying_symbol": "STOCKBB",
            "action": "Buy to Open",
            "quantity": Decimal("1.0"),
            "price": Decimal("40.3989"),
            "regulatory_fees": Decimal("0.0"),
            "clearing_fees": Decimal("-0.001"),
            "commission": Decimal("0.0"),
            "proprietary_index_option_fees": Decimal("0.0"),
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
    ),
]

forward_split = [
    Transaction(
        **{
            "account_number": "6VV78917",
            "action": "Sell to Close",
            "agency_price": None,
            "clearing_fees": None,
            "commission": None,
            "cost_basis_reconciliation_date": None,
            "description": "Forward split: Close 1.0 STOCKA",
            "destination_venue": None,
            "exchange": None,
            "exchange_affiliation_identifier": None,
            "exec_id": None,
            "executed_at": datetime.datetime(
                2023, 9, 28, 18, 36, 20, 28000, tzinfo=datetime.timezone.utc
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
            "net_value": Decimal("40.4"),
            "order_id": None,
            "other_charge": None,
            "other_charge_description": None,
            "other_charge_effect": None,
            "price": None,
            "principal_price": None,
            "proprietary_index_option_fees": None,
            "quantity": Decimal("1.0"),
            "regulatory_fees": None,
            "reverses_id": None,
            "symbol": "STOCKA",
            "transaction_date": datetime.datetime(2023, 9, 28),
            "transaction_sub_type": "Forward Split",
            "transaction_type": "Receive Deliver",
            "underlying_symbol": "STOCKA",
            "value": Decimal("40.4"),
        }
    ),
    Transaction(
        **{
            "account_number": "6VV78917",
            "action": "Buy to Open",
            "agency_price": None,
            "clearing_fees": None,
            "commission": None,
            "cost_basis_reconciliation_date": None,
            "description": "Forward split: Open 2.0 STOCKA",
            "destination_venue": None,
            "exchange": None,
            "exchange_affiliation_identifier": None,
            "exec_id": None,
            "executed_at": datetime.datetime(
                2023, 9, 28, 18, 36, 21, 28000, tzinfo=datetime.timezone.utc
            ),
            "ext_exchange_order_number": None,
            "ext_exec_id": None,
            "ext_global_order_number": None,
            "ext_group_fill_id": None,
            "ext_group_id": None,
            "id": 274072376,
            "instrument_type": InstrumentType.EQUITY,
            "is_estimated_fee": True,
            "leg_count": None,
            "lots": None,
            "net_value": Decimal("40.4"),
            "order_id": None,
            "other_charge": None,
            "other_charge_description": None,
            "other_charge_effect": None,
            "price": None,
            "principal_price": None,
            "proprietary_index_option_fees": None,
            "quantity": Decimal("2.0"),
            "regulatory_fees": None,
            "reverses_id": None,
            "symbol": "STOCKA",
            "transaction_date": datetime.datetime(2023, 9, 28),
            "transaction_sub_type": "Forward Split",
            "transaction_type": "Receive Deliver",
            "underlying_symbol": "STOCKA",
            "value": Decimal("40.4"),
        }
    ),
]


dividends = [
    Transaction(
        **{
            "account_number": "6VV78917",
            "action": None,
            "agency_price": None,
            "clearing_fees": None,
            "commission": None,
            "cost_basis_reconciliation_date": None,
            "description": "COMPANY B",
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
            "order_id": None,
            "other_charge": None,
            "other_charge_description": None,
            "other_charge_effect": None,
            "price": None,
            "principal_price": None,
            "proprietary_index_option_fees": None,
            "quantity": None,
            "regulatory_fees": None,
            "reverses_id": None,
            "symbol": "STOCKA",
            "transaction_date": datetime.date(2023, 12, 15),
            "transaction_sub_type": "Dividend",
            "transaction_type": "Money Movement",
            "underlying_symbol": "STOCKA",
            "value": Decimal("0.96"),
        }
    ),
    Transaction(
        **{
            "account_number": "6VV78917",
            "action": None,
            "agency_price": None,
            "clearing_fees": None,
            "commission": None,
            "cost_basis_reconciliation_date": None,
            "description": "COMPANY B",
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
            "net_value": Decimal("-0.14"),
            "order_id": None,
            "other_charge": None,
            "other_charge_description": None,
            "other_charge_effect": None,
            "price": None,
            "principal_price": None,
            "proprietary_index_option_fees": None,
            "quantity": None,
            "regulatory_fees": None,
            "reverses_id": None,
            "symbol": "STOCKA",
            "transaction_date": datetime.date(2023, 12, 15),
            "transaction_sub_type": "Dividend",
            "transaction_type": "Money Movement",
            "underlying_symbol": "STOCKA",
            "value": Decimal("-0.14"),
        }
    ),
]


dividend_reinvestment_transaction_buy = Transaction(
    **{
        "account_number": "6VV78917",
        "action": "Buy to Open",
        "agency_price": None,
        "clearing_fees": None,
        "commission": None,
        "cost_basis_reconciliation_date": None,
        "description": "Received 0.01391 Long STOCKA via Dividend",
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
        "order_id": None,
        "other_charge": None,
        "other_charge_description": None,
        "other_charge_effect": None,
        "price": Decimal("59.04"),
        "principal_price": None,
        "proprietary_index_option_fees": None,
        "quantity": Decimal("0.01391"),
        "regulatory_fees": None,
        "reverses_id": None,
        "symbol": "STOCKA",
        "transaction_date": datetime.date(2023, 12, 15),
        "transaction_sub_type": "Dividend",
        "transaction_type": "Receive Deliver",
        "underlying_symbol": "STOCKA",
        "value": Decimal("0.0"),
    }
)


divident_reinvestment = [
    dividend_reinvestment_transaction_buy,
    Transaction(
        **{
            "account_number": "6VV78917",
            "action": None,
            "agency_price": None,
            "clearing_fees": None,
            "commission": None,
            "cost_basis_reconciliation_date": None,
            "description": "Cash dividend reinvested info STOCKA",
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
            "order_id": None,
            "other_charge": None,
            "other_charge_description": None,
            "other_charge_effect": None,
            "price": None,
            "principal_price": None,
            "proprietary_index_option_fees": None,
            "quantity": None,
            "regulatory_fees": None,
            "reverses_id": None,
            "symbol": "STOCKA",
            "transaction_date": datetime.date(2023, 12, 15),
            "transaction_sub_type": "Withdrawal",
            "transaction_type": "Money Movement",
            "underlying_symbol": "STOCKA",
            "value": Decimal("0.82"),
        }
    ),
]


symbol_change_sell_old = Transaction(
    **{
        "account_number": "6VV78917",
        "action": "Sell to Close",
        "agency_price": None,
        "clearing_fees": None,
        "commission": None,
        "cost_basis_reconciliation_date": None,
        "description": "Symbol change:  Close 5.47124 STOCKB",
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
        "order_id": None,
        "other_charge": None,
        "other_charge_description": None,
        "other_charge_effect": None,
        "price": None,
        "principal_price": None,
        "proprietary_index_option_fees": None,
        "quantity": Decimal("5.47124"),
        "regulatory_fees": None,
        "reverses_id": None,
        "symbol": "STOCKB",
        "transaction_date": datetime.date(2024, 7, 15),
        "transaction_sub_type": "Symbol Change",
        "transaction_type": "Receive Deliver",
        "underlying_symbol": "STOCKB",
        "value": Decimal("82.165"),
    }
)


symbol_change_buy_new = Transaction(
    **{
        "account_number": "6VV78917",
        "action": "Buy to Open",
        "agency_price": None,
        "clearing_fees": None,
        "commission": None,
        "cost_basis_reconciliation_date": None,
        "description": "Symbol change:  Open 5.47124 STOCKB",
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
        "order_id": None,
        "other_charge": None,
        "other_charge_description": None,
        "other_charge_effect": None,
        "price": None,
        "principal_price": None,
        "proprietary_index_option_fees": None,
        "quantity": Decimal("5.47124"),
        "regulatory_fees": None,
        "reverses_id": None,
        "symbol": "STOCKBB",
        "transaction_date": datetime.date(2024, 7, 15),
        "transaction_sub_type": "Symbol Change",
        "transaction_type": "Receive Deliver",
        "underlying_symbol": "STOCKBB",
        "value": Decimal("82.165"),
    }
)


TRANSACTIONS = [
    *dividends,
    *divident_reinvestment,
    *forward_split,
    symbol_change_buy_new,
    symbol_change_sell_old,
    *trade_buys,
]
