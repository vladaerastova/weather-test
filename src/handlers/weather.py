from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from src.services import weather_service
from src.common.db import get_db, Session

router = APIRouter()

security = APIKeyHeader(name="x-token", auto_error=False)


@router.get("/temperature/{date}")
async def temperature_by_date(date: str, session: Session = Depends(get_db), x_token: str = Depends(security)):
    if not x_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")

    return await weather_service.temperature_by_date(session, date)
