from pydantic import BaseModel


class SymbolChange(BaseModel):
    old_symbol: str
    new_symbol: str
