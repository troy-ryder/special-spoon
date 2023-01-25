from unicodedata import decimal
from pydantic import BaseModel
from accounts.models.customer import Customer


class Account(BaseModel):
    id: int
    number: str
    customer_id: Customer
    balance: float

