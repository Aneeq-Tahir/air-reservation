from fastapi import FastAPI, HTTPException, Depends
from .database import (
    SQLModel,
    engine,
    get_session,
    Customer,
    FlightTicket,
    Schedule,
    Reservation,
    Session,
)
from sqlmodel import select
from typing import List, Annotated


def lifespan(app: FastAPI):
    print("Creating Database Tables...")
    SQLModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

session_type = Annotated[Session, Depends(get_session)]


@app.post("/customers/", response_model=Customer)
async def create_customer(customer: Customer, session: session_type):
    try:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/customers/", response_model=List[Customer])
async def read_customers(session: session_type):
    try:
        customers = session.exec(select(Customer)).all()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/customers/{customer_id}", response_model=Customer)
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


@app.delete("/customers/{customer_id}")
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


@app.post("/flight_tickets/", response_model=FlightTicket)
async def create_flight_ticket(flight_ticket: FlightTicket, session: session_type):
    try:
        session.add(flight_ticket)
        session.commit()
        session.refresh(flight_ticket)
        return flight_ticket
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/flight_tickets/", response_model=List[FlightTicket])
async def read_flight_tickets(session: session_type):
    try:
        flight_tickets = session.exec(select(FlightTicket)).all()
        return flight_tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/flight_tickets/{ticket_id}", response_model=FlightTicket)
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


@app.delete("/flight_tickets/{ticket_id}")
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


@app.post("/schedules/", response_model=Schedule)
async def create_schedule(schedule: Schedule, session: session_type):
    try:
        session.add(schedule)
        session.commit()
        session.refresh(schedule)
        return schedule
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/schedules/", response_model=List[Schedule])
async def read_schedules(session: session_type):
    try:
        schedules = session.exec(select(Schedule)).all()
        return schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/schedules/{schedule_id}", response_model=Schedule)
async def update_schedule(schedule_id: int, schedule: Schedule, session: session_type):
    try:
        db_schedule = session.exec(
            select(Schedule).where(Schedule.id == schedule_id)
        ).first()
        if not db_schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
        for field in Schedule.model_fields:
            field_value = getattr(schedule, field)
            if field_value is not None:
                setattr(db_schedule, field, field_value)
        session.commit()
        session.refresh(db_schedule)
        return db_schedule
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/schedules/{schedule_id}")
async def delete_schedule(schedule_id: int, session: session_type):
    try:
        schedule = session.exec(
            select(Schedule).where(Schedule.id == schedule_id)
        ).first()
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
        session.delete(schedule)
        session.commit()
        return {"ok": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reservations/", response_model=Reservation)
async def create_reservation(reservation: Reservation, session: session_type):
    try:
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        return reservation
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reservations/", response_model=List[Reservation])
async def read_reservations(session: session_type):
    try:
        reservations = session.exec(select(Reservation)).all()
        return reservations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/reservations/{reservation_id}", response_model=Reservation)
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


@app.delete("/reservations/{reservation_id}")
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
