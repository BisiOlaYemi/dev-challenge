from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class WeatherHour(BaseModel):
    """Represents weather data for a specific hour."""
    hour: int = Field(..., ge=0, le=23)
    temperature: str
    condition: str

class WeatherResponse(BaseModel):
    """Response model for the /weather endpoint."""
    city: str
    date: date
    weather: List[WeatherHour]
    source: str  
    error: Optional[str] = None 