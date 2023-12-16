from pydantic import BaseModel, ConfigDict, Field


class GhostfolioActivity(BaseModel):
    account_id: str = Field(..., alias="accountId")
    comment: str | None
    currency: str
    data_source: str | None = Field(None, alias="dataSource", exclude=True)
    date: str
    fee: float
    id: str | None = Field(None, exclude=True)
    quantity: float
    symbol: str
    type: str
    unit_price: float = Field(..., alias="unitPrice")

    class Config:
        allow_population_by_field_name = True
