from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import get_all_cities
from cities.schemas import SCity
from database import get_async_session

router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/")
async def get_cities(session: AsyncSession = Depends(get_async_session)) -> List[SCity]:
    cities = await get_all_cities(session)
    return [SCity.model_validate(city) for city in cities]
