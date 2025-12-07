from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.dependencies import get_db
from src.modules.payments import schemas, services


router = APIRouter()

@router.post("/", response_model=schemas.PaymentBase)
async def create_payment(payment_in: schemas.PaymentCreate, db: AsyncSession = Depends(get_db)):
    return await services.create_payment(db, payment_in)


@router.get("/", response_model=list[schemas.PaymentBase])
async def read_payments(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await services.get_payments(db, skip, limit)


@router.get("/{payment_id}", response_model=schemas.PaymentBase)
async def read_payment(payment_id: int, db: AsyncSession = Depends(get_db)):
    return await services.get_payment(db, payment_id)


@router.put("/{payment_id}", response_model=schemas.PaymentBase)
async def update_payment(payment_id: int, payment_in: schemas.PaymentUpdate, db: AsyncSession = Depends(get_db)):
    return await services.update_payment(db, payment_id, payment_in)


@router.delete("/{payment_id}")
async def delete_payment(payment_id: int, db: AsyncSession = Depends(get_db)):
    return await services.delete_payment(db, payment_id)
