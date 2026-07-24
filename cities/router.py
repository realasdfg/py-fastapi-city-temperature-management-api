from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities.crud import create_city, get_all_cities
from cities.schemas import SCity, SCityCreate
from database import get_async_session

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/")
async def add_city(
    city_data: SCityCreate,
    session: AsyncSession = Depends(get_async_session),
) -> SCity:
    city = await create_city(session, data=city_data)
    return SCity.model_validate(city)


@router.get("/")
async def get_cities(session: AsyncSession = Depends(get_async_session)) -> List[SCity]:
    cities = await get_all_cities(session=session)
    return [SCity.model_validate(city) for city in cities]
