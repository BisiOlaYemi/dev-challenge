import pytest
from fastapi.testclient import TestClient
from main import app
import external_api
from cache import WeatherCache

client = TestClient(app)

def test_weather_valid_city(monkeypatch):
    # Mock external API to always return data
    monkeypatch.setattr(external_api, "fetch_weather_from_external_api", lambda city: [
        {"hour": h, "temperature": "20", "condition": "Clear"} for h in range(24)
    ])
    response = client.get("/weather?city=Berlin")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Berlin"
    assert len(data["weather"]) == 24
    assert data["source"] in ("external", "cache")

def test_weather_cache(monkeypatch):
    monkeypatch.setattr(external_api, "fetch_weather_from_external_api", lambda city: [
        {"hour": h, "temperature": "21", "condition": "Clear"} for h in range(24)
    ])
    client.get("/weather?city=Paris")
    # simulate external API failure
    monkeypatch.setattr(external_api, "fetch_weather_from_external_api", lambda city: None)
    response = client.get("/weather?city=Paris")
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "cache"
    assert data["error"] is None or "cached" in data["error"].lower()

def test_weather_external_api_failure(monkeypatch):
    WeatherCache().clear()
    # No cache fails
    monkeypatch.setattr("main.fetch_weather_from_external_api", lambda city: None)
    response = client.get("/weather?city=NowhereUniqueTestCity")
    assert response.status_code == 503
    assert "unavailable" in response.json()["detail"].lower()

def test_weather_invalid_city():
    response = client.get("/weather?city=")
    assert response.status_code == 422
    response = client.get("/weather?city=" + "a"*101)
    assert response.status_code == 422 