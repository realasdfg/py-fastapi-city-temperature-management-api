from sqlalchemy.ext.asyncio import AsyncSession

from temperatures.models import Temperature
from temperatures.schemas import STemperatureCreate


async def create_temperatures(
    session: AsyncSession, data: list[STemperatureCreate]
) -> list[Temperature]:
    temperatures = [Temperature(**item.model_dump()) for item in data]
    session.add_all(temperatures)
    await session.flush()
    return temperatures
