from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from tastytrade_ghostfolio.core.entity.transaction_type import TransactionType


class Trade(BaseModel):
    description: Optional[str] = Field(None)
    executed_at: datetime
    fee: Decimal
    id: Optional[str] = Field(None)
    quantity: Decimal
    symbol: str
    transaction_type: TransactionType
    unit_price: Decimal

    def change_symbol(self, value: str):
        self.symbol = value
