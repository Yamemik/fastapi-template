from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.modules.payments.models import Payment
from src.modules.payments.schemas import PaymentCreate, PaymentUpdate


async def get_payment(db: AsyncSession, payment_id: int):
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    return result.scalar_one_or_none()


async def get_payments(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Payment).offset(skip).limit(limit))
    return result.scalars().all()


async def create_payment(db: AsyncSession, payment: PaymentCreate):
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment


async def update_payment(db: AsyncSession, payment_id: int, payment_data: PaymentUpdate):
    db_payment = await get_payment(db, payment_id)
    if not db_payment:
        return None

    update_data = payment_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_payment, key, value)

    await db.commit()
    await db.refresh(db_payment)
    return db_payment


async def delete_payment(db: AsyncSession, payment_id: int):
    db_payment = await get_payment(db, payment_id)
    if db_payment:
        await db.delete(db_payment)
        await db.commit()
        return True
    return False
