from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession

from cities.models import City
from cities.schemas import SCityCreate


async def create_city(session: AsyncSession, data: SCityCreate) -> City:
    city = City(**data.model_dump())
    session.add(city)
    await session.flush()
    await session.refresh(city)
    return city


async def get_all_cities(session: AsyncSession) -> Sequence[City]:
    stmt = select(City)
    result = await session.execute(stmt)
    return result.scalars().all()
