from datetime import datetime

from pydantic import BaseModel


class STemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class STemperature(STemperatureBase):
    id: int

    class Config:
        from_attributes = True


class STemperatureCreate(STemperatureBase):
    pass
