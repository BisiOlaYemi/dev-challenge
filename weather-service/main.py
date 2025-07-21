from fastapi import FastAPI, HTTPException, Query, Depends
from datetime import date
from typing import Optional

from models import WeatherResponse, WeatherHour
from cache import WeatherCache
from external_api import fetch_weather_from_external_api
from config import settings

app = FastAPI(title="Weather Service")

@app.get("/weather", response_model=WeatherResponse)
def get_weather(
    city: str = Query(..., min_length=1, max_length=100),
    cache: WeatherCache = Depends(WeatherCache),
    config = Depends(lambda: settings)
):
    today = date.today()
    cache_entry = cache.get(city, today, config.CACHE_TTL)
    if cache_entry:
        return WeatherResponse(
            city=city,
            date=today,
            weather=cache_entry['data'],
            source="cache"
        )
    weather_data = fetch_weather_from_external_api(city)
    if weather_data is not None:
        weather_hours = [WeatherHour(**item) for item in weather_data]
        cache.set(city, today, weather_hours)
        return WeatherResponse(
            city=city,
            date=today,
            weather=weather_hours,
            source="external"
        )
    # If the external API failed, try to serve stale cache available
    cache_entry = cache.get(city, today, config.CACHE_TTL * 24) 
    if cache_entry:
        print(f"[DEBUG] Serving stale cache for city={city}, date={cache_entry['date']}")
        return WeatherResponse(
            city=city,
            date=cache_entry['date'],
            weather=cache_entry['data'],
            source="cache",
            error="External API unavailable, served cached data."
        )
    raise HTTPException(status_code=503, detail="Weather data unavailable for this city.")
