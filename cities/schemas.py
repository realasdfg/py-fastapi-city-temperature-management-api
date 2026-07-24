from pydantic import BaseModel


class SCityBase(BaseModel):
    name: str
    additional_info: str


class SCity(SCityBase):
    id: int


class SCityCreate(SCityBase):
    pass
