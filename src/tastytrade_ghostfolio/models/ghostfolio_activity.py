from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TransactionType(Enum):
    BUY = "BUY"
    DIVIDEND = "DIVIDEND"
    FEE = "FEE"
    INTEREST = "INTEREST"
    ITEM = "ITEM"
    LIABILITY = "LIABILITY"
    SELL = "SELL"


class GhostfolioActivity(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account_id: Optional[str] = Field(None, alias="accountId")
    comment: Optional[str] = None
    currency: str
    data_source: Optional[str] = Field(None, alias="dataSource", exclude=True)
    date: date
    fee: float
    id: Optional[str] = Field(None, exclude=True)
    quantity: float
    symbol: str
    type: TransactionType
    unit_price: float = Field(..., alias="unitPrice")
