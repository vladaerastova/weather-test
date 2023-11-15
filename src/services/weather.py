from datetime import datetime
from aiohttp import ClientSession
from src.common.logger import module_logger
from src.common.db import TemperatureRecord
from sqlalchemy import func
from typing import Tuple
from fastapi import status
import os

logger = module_logger(__name__)


class WeatherService:

    def __init__(self):
        self.city = os.environ.get("CITY")
        self.api_key = os.environ.get("API_KEY")

    async def get_temperature(self, city: str):
        url = "https://api.openweathermap.org/data/2.5/weather"
        lat, lon = await self.get_lat_lon(city)
        params = {'lat': lat, 'lon': lon, 'appid': self.api_key, 'units': 'metric'}
        try:
            async with ClientSession() as session, session.get(url, params=params) as response:
                if response.status == status.HTTP_200_OK:
                    weather_data = await response.json()
                    temperature = weather_data.get("main", {}).get("temp")
                    timestamp = datetime.fromtimestamp(weather_data.get("dt"))
                    logger.info(f"Successfully getting temperature for {city}: {temperature}")
                    return temperature, timestamp
                else:
                    logger.error(f"Status code {response.status}, msg {response.json()}")
        except Exception as ex:
            logger.error(f"Gor error while getting temperature for {city} with params {params}: {ex}")

    async def get_lat_lon(self, city: str = None) -> Tuple[float, float]:
        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {"q": self.city, "appid": self.api_key, "limit": 1}
        try:
            async with ClientSession() as session, session.get(url, params=params) as response:
                if response.status == status.HTTP_200_OK:
                    data = await response.json()
                    if data:
                        lat = data[0].get("lat")
                        lon = data[0].get("lon")
                        logger.info(f"Successfully getting location for {city}: {lat}, {lon}")
                        return lat, lon
                else:
                    logger.error(f"Status {response.status}, {response.__repr__()}")
        except Exception as ex:
            logger.error(f"Gor error {ex}")

    async def save_weather_data(self, session):
        temperature, timestamp = await self.get_temperature(self.city)
        session.add(TemperatureRecord(city=self.city, temperature=temperature, timestamp=timestamp))
        session.commit()

    async def temperature_by_date(self, session, date):
        temp = session.query(TemperatureRecord).filter(func.DATE(TemperatureRecord.timestamp) == date).all()
        return temp


