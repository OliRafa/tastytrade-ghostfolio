from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class TransactionType(Enum):
    BUY = "BUY"
    DIVIDEND = "DIVIDEND"
    FEE = "FEE"
    INTEREST = "INTEREST"
    ITEM = "ITEM"
    LIABILITY = "LIABILITY"
    SELL = "SELL"


class GhostfolioActivity(BaseModel):
    account_id: str | None = Field(None, alias="accountId")
    comment: str | None
    currency: str
    data_source: str | None = Field(None, alias="dataSource", exclude=True)
    date: date
    fee: float
    id: str | None = Field(None, exclude=True)
    quantity: float
    symbol: str
    type: TransactionType
    unit_price: float = Field(..., alias="unitPrice")

    class Config:
        allow_population_by_field_name = True
