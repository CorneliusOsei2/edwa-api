from pydantic import BaseModel


class BusinessBase(BaseModel):
    name: str
    location: str
    email: str
    phone_number: str
    trade_in: str


class BusinessIn(BusinessBase):
    ...
