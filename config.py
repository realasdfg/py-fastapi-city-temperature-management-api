from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    db_uri: str
    weatherapi_key: str


settings = Settings()
