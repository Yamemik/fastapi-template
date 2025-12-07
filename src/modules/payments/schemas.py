from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class PaymentBase(BaseModel):
    title: str


class PaymentCreate(PaymentBase):
    user_id: int


class PaymentUpdate(BaseModel):
    title: Optional[str] = None


class PaymentRead(PaymentBase):
    id: int
    created_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)
