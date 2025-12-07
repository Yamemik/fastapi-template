from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Payment
from .schemas import PaymentCreate, PaymentUpdate


async def get_payment(db: AsyncSession, payment_id: int) -> Optional[Payment]:
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    return result.scalar_one_or_none()


async def list_payments(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Payment]:
    result = await db.execute(select(Payment).offset(skip).limit(limit))
    return result.scalars().all()


async def create_payment(db: AsyncSession, payload: PaymentCreate) -> Payment:
    db_obj = Payment(title=payload.title, user_id=payload.user_id)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_payment(db: AsyncSession, payment_id: int, payload: PaymentUpdate) -> Optional[Payment]:
    pay = await get_payment(db, payment_id)
    if not pay:
        return None
    data = payload.model_dump(exclude_none=True)
    for k, v in data.items():
        setattr(pay, k, v)
    db.add(pay)
    await db.commit()
    await db.refresh(pay)
    return pay


async def delete_payment(db: AsyncSession, payment_id: int) -> bool:
    pay = await get_payment(db, payment_id)
    if not pay:
        return False
    await db.delete(pay)
    await db.commit()
    return True
