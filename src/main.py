from fastapi import FastAPI
from .database import SQLModel, engine
from .routers import customer, reservation, schedule, ticket


def lifespan(app: FastAPI):
    print("Creating Database Tables...")
    SQLModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(customer.router)
app.include_router(reservation.router)
app.include_router(schedule.router)
app.include_router(ticket.router)
