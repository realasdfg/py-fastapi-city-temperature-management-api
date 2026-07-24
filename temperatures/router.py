import asyncio
from datetime import datetime

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import get_all_cities
from database import get_async_session
from temperatures.crud import create_temperatures
from temperatures.schemas import (
    STemperatureCreate,
    STemperatureUpdateResult,
)
from temperatures.weather_client import WeatherFetchError, fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update/")
async def update_temperatures(
    session: AsyncSession = Depends(get_async_session),
) -> list[STemperatureUpdateResult]:
    cities = await get_all_cities(session)

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_current_temperature(client, city.name) for city in cities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    now = datetime.utcnow()
    to_create: list[STemperatureCreate] = []
    response: list[STemperatureUpdateResult] = []

    for city, result in zip(cities, results):
        if isinstance(result, WeatherFetchError):
            response.append(
                STemperatureUpdateResult(
                    city_id=city.id,
                    city_name=city.name,
                    success=False,
                    error=str(result),
                )
            )
            continue
        if isinstance(result, Exception):
            response.append(
                STemperatureUpdateResult(
                    city_id=city.id,
                    city_name=city.name,
                    success=False,
                    error=f"Unexpected error: {result}",
                )
            )
            continue

        temperature: float = result
        to_create.append(
            STemperatureCreate(city_id=city.id, date_time=now, temperature=temperature)
        )
        response.append(
            STemperatureUpdateResult(
                city_id=city.id,
                city_name=city.name,
                success=True,
                temperature=temperature,
            )
        )

    if to_create:
        await create_temperatures(session, to_create)
        await session.commit()

    return response
