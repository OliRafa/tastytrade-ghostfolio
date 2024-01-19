from pydantic import BaseModel, Field


class GhostfolioAccount(BaseModel):
    account_id: str | None = Field(None, alias="id", exclude=True)
    account_type: str = Field("SECURITIES", alias="accountType", exclude=True)
    balance: float = 0.0
    balance_in_base_currency: float = Field(
        0.0, alias="balanceInBaseCurrency", exclude=True
    )
    currency: str = "USD"
    id: str | None = Field(None, exclude=True)
    name: str
    platform_id: str | None = Field(None, alias="platformId")
    comment: str | None = "Created by Tastytrade-Ghostfolio."

    class Config:
        allow_population_by_field_name = True
