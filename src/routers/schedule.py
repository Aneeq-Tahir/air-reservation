from fastapi import APIRouter, HTTPException
from sqlmodel import select
from src.database import Schedule, session_type
from typing import List

router = APIRouter()


@router.post("/schedules/", response_model=Schedule)
async def create_schedule(schedule: Schedule, session: session_type):
    try:
        session.add(schedule)
        session.commit()
        session.refresh(schedule)
        return schedule
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedules/", response_model=List[Schedule])
async def read_schedules(session: session_type):
    try:
        schedules = session.exec(select(Schedule)).all()
        return schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/schedules/{schedule_id}", response_model=Schedule)
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


@router.delete("/schedules/{schedule_id}")
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
