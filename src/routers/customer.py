from fastapi import APIRouter, HTTPException
from sqlmodel import select
from src.database import Customer, session_type
from typing import List

router = APIRouter()


@router.post("/customer", response_model=Customer)
async def create_customer(customer: Customer, session: session_type):
    try:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer", response_model=List[Customer])
async def read_customers(session: session_type):
    try:
        customers = session.exec(select(Customer)).all()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/customer/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer: Customer, session: session_type):
    try:
        db_customer = session.exec(
            select(Customer).where(Customer.id == customer_id)
        ).first()
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        for field in Customer.model_fields:
            field_value = getattr(customer, field)
            if field_value is not None:
                setattr(db_customer, field, field_value)
        session.commit()
        session.refresh(db_customer)
        return db_customer
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/customer/{customer_id}")
async def delete_customer(customer_id: int, session: session_type):
    try:
        customer = session.exec(
            select(Customer).where(Customer.id == customer_id)
        ).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        session.delete(customer)
        session.commit()
        return {"ok": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
