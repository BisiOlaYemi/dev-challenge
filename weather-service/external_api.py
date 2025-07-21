from typing import List, Optional
from rate_limiter import RateLimiter
from datetime import timedelta

rate_limiter = RateLimiter(100, timedelta(hours=1))

def fetch_weather_from_external_api(city: str) -> Optional[List[dict]]:
    """
    This function acts as a placeholder for making a real HTTP request to an external weather API.
    For now, it randomly simulates success or failure, and also respects a rate limit of 100 requests per hour.
    In production, I would swap this out for an actual API call, handling errors and timeouts robustly.
    If the rate limit is hit or a simulated failure occurs, it returns None to mimic an unavailable service.
    """
    if not rate_limiter.allow():
        return None
    import random
    if random.random() < 0.1:
        return None
    return [
        {"hour": h, "temperature": str(18 - h // 3), "condition": "Clear" if h < 20 else "Cloudy"}
        for h in range(24)
    ] 