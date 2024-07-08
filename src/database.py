from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session, Field
from pydantic import EmailStr
from typing import Optional, Annotated
from datetime import datetime

DATABASE_URL = "postgresql+psycopg://aneeq:aneeqtahir@localhost:5432/aneeqdb"
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


session_type = Annotated[Session, Depends(get_session)]


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    gender: str
    age: int
    cust_email: EmailStr = Field(unique=True)
    cust_pass: str


class FlightTicket(SQLModel, table=True):
    __tablename__ = "flight_tickets"

    id: Optional[int] = Field(default=None, primary_key=True)
    cust_id: int = Field(foreign_key="customers.id")
    schedule_id: int = Field(foreign_key="schedules.id")
    seat_num: int
    class_type: str
    origin: str
    destination: str


class Schedule(SQLModel, table=True):
    __tablename__ = "schedules"

    id: Optional[int] = Field(default=None, primary_key=True)
    flight_date: str
    time_depart: datetime
    time_arrive: datetime


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"

    id: Optional[int] = Field(default=None, primary_key=True)
    cust_id: int = Field(foreign_key="customers.id")
    ticket_id: int = Field(foreign_key="flight_tickets.id")
    date_reserved: datetime = Field(default_factory=datetime.utcnow)
