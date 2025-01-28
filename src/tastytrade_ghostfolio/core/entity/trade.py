from datetime import datetime
from decimal import Decimal
from typing import Optional, Self

from pydantic import BaseModel, Field, computed_field

from tastytrade_ghostfolio.core.entity.transaction_type import TransactionType


class Trade(BaseModel):
    description: Optional[str] = Field(None)
    executed_at: datetime
    fee: Decimal
    id: Optional[str] = Field(None)
    inner_quantity: Optional[Decimal] = Field(
        None, alias="quantity", exclude=True, repr=False
    )
    symbol: str
    transaction_type: TransactionType
    unit_price: Decimal
    value: Optional[Decimal] = Field(None)

    def change_symbol(self, value: str):
        self.symbol = value

    @computed_field
    @property
    def quantity(self) -> Decimal:
        if self.inner_quantity is None:
            return round(self.value / self.unit_price, 14)

        return self.inner_quantity

    @quantity.setter
    def quantity(self, value: Decimal):
        self.inner_quantity = value

    def __eq__(self, other: datetime | Self) -> bool:
        """To implement 'in' operator"""
        if (
            self.executed_at.date() == other.executed_at.date()
            and self.quantity == other.quantity
            and self.symbol == other.symbol
            and self.unit_price == other.unit_price
        ):
            return True

        return False
