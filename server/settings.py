from typing import Annotated
from typing import Optional

from pydantic import Field 
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    host: Annotated[str, Field(default="localhost")]
    port: Annotated[int, Field(default=27017)]

class Settings(BaseSettings):
    database: Annotated[DatabaseSettings, Field(default_factory=DatabaseSettings)]