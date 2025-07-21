import threading
from datetime import datetime, date, timedelta, timezone
from typing import Dict, Any, Optional

class WeatherCache:
    """implementation of in-memory cache for weather data, per city per day."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._cache = {}
                    cls._instance._cache_lock = threading.Lock()
        return cls._instance

    def get(self, city: str, today: date, ttl: timedelta) -> Optional[Dict[str, Any]]:
        key = city.lower().strip()
        now = datetime.now(timezone.utc)
        with self._cache_lock:
            entry = self._cache.get(key)
            if entry and entry['date'] == today and now - entry['timestamp'] < ttl:
                return entry
        return None

    def set(self, city: str, today: date, data: Any):
        key = city.lower().strip()
        now = datetime.now(timezone.utc)
        with self._cache_lock:
            self._cache[key] = {
                'date': today,
                'data': data,
                'timestamp': now
            }

    def clear(self):
        """Clear the entire weather cache. Useful for testing and operational resets."""
        with self._cache_lock:
            self._cache.clear() 