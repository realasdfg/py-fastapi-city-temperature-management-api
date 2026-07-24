from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession

from cities.models import City


async def get_all_cities(session: AsyncSession) -> Sequence[City]:
    stmt = select(City)
    result = await session.execute(stmt)
    return result.scalars().all()
