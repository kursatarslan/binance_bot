from pydantic import BaseModel

class OrderRequest(BaseModel):
    symbol: str
    quantity: float
