import uvicorn
from fastapi import FastAPI, Depends
from fastapi_utils.tasks import repeat_every
from src.handlers.weather import router
from src.common.helpers import verify_token
from src.common.db import get_db
from src.services import weather_service

app = FastAPI(dependencies=[Depends(verify_token)])
app.include_router(router)


@app.on_event("startup")
@repeat_every(seconds=60 * 60)
async def on_startup():
    await weather_service.save_weather_data(next(get_db()))


# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000)
