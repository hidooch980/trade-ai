from pydantic import BaseModel

class Symbol(BaseModel):
    name: str
    market: str
    active: bool = True
