from fastapi import APIRouter, HTTPException
from sqlmodel import select
from src.database import FlightTicket, session_type
from typing import List

router = APIRouter()


@router.post("/ticket/", response_model=FlightTicket)
async def create_flight_ticket(flight_ticket: FlightTicket, session: session_type):
    try:
        session.add(flight_ticket)
        session.commit()
        session.refresh(flight_ticket)
        return flight_ticket
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ticket/", response_model=List[FlightTicket])
async def read_flight_tickets(session: session_type):
    try:
        flight_tickets = session.exec(select(FlightTicket)).all()
        return flight_tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/ticket/{ticket_id}", response_model=FlightTicket)
async def update_flight_ticket(
    ticket_id: int, flight_ticket: FlightTicket, session: session_type
):
    try:
        ticket = session.exec(
            select(FlightTicket).where(FlightTicket.id == ticket_id)
        ).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="FlightTicket not found")
        for field in FlightTicket.model_fields:
            field_value = getattr(flight_ticket, field)
            if field_value is not None:
                setattr(ticket, field, field_value)
        session.commit()
        session.refresh(ticket)
        return ticket
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/ticket/{ticket_id}")
async def delete_flight_ticket(ticket_id: int, session: session_type):
    try:
        ticket = session.exec(
            select(FlightTicket).where(FlightTicket.id == ticket_id)
        ).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="FlightTicket not found")
        session.delete(ticket)
        session.commit()
        return {"ok": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
