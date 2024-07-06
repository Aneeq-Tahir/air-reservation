from fastapi import APIRouter, HTTPException
from sqlmodel import select
from src.database import Reservation, session_type
from typing import List

router = APIRouter()


@router.post("/reservations/", response_model=Reservation)
async def create_reservation(reservation: Reservation, session: session_type):
    try:
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        return reservation
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reservations/", response_model=List[Reservation])
async def read_reservations(session: session_type):
    try:
        reservations = session.exec(select(Reservation)).all()
        return reservations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/reservations/{reservation_id}", response_model=Reservation)
async def update_reservation(
    reservation_id: int, reservation: Reservation, session: session_type
):
    try:
        db_reservation = session.exec(
            select(Reservation).where(Reservation.id == reservation_id)
        ).first()
        if not db_reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        for field in Reservation.model_fields:
            field_value = getattr(reservation, field)
            if field_value is not None and field_value != "date_reserved":
                setattr(db_reservation, field, field_value)
        session.commit()
        session.refresh(db_reservation)
        return db_reservation
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int, session: session_type):
    try:
        reservation = session.exec(
            select(Reservation).where(Reservation.id == reservation_id)
        ).first()
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        session.delete(reservation)
        session.commit()
        return {"ok": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
