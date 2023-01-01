from datetime import datetime
from pydantic import BaseModel


class ClientBase(BaseModel):
    name: str
    location: str
    email: str
    phone_number: str
    trade_in: str
    full_name: str
    username: str
    is_active: bool = False
    company_name: str = ""
    is_business: bool = False
    start_date: datetime = datetime.now()


class ClientIn(ClientBase):
    ...
