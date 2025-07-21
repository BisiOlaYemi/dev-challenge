from pydantic_settings import BaseSettings
from pydantic import Field
from datetime import timedelta

class Settings(BaseSettings):
    """Application configuration loaded from environment variables or defaults."""
    CACHE_TTL_HOURS: int = Field(1, description="Cache TTL in hours") 
    EXTERNAL_API_TIMEOUT: int = Field(5, description="External API timeout in seconds")
    

    @property
    def CACHE_TTL(self) -> timedelta:
        return timedelta(hours=self.CACHE_TTL_HOURS)

settings = Settings() 