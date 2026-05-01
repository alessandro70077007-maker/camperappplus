"""Meteo via Open-Meteo (no API key, gratis). Cache 30 min."""
import hashlib
import json
import time
from pathlib import Path

import requests

import storage


CACHE_TTL = 30 * 60  # 30 min
CACHE_DIR = storage.DATA_DIR / "weather_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

ENDPOINT = "https://api.open-meteo.com/v1/forecast"
GEOCODE_ENDPOINT = "https://geocoding-api.open-meteo.com/v1/search"


def geocode(query: str, language: str = "it") -> tuple[float, float, str] | None:
    """Cerca lat/lon per nome citta/luogo. Ritorna (lat, lon, display_name) o None.
    Usa Open-Meteo geocoding (gratis, no API key)."""
    q = query.strip()
    if not q:
        return None
    try:
        resp = requests.get(
            GEOCODE_ENDPOINT,
            params={"name": q, "count": 1, "language": language},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return None
    results = data.get("results") or []
    if not results:
        return None
    r = results[0]
    name_parts = [r.get("name", "")]
    if r.get("admin1"):
        name_parts.append(r["admin1"])
    if r.get("country"):
        name_parts.append(r["country"])
    display = ", ".join(p for p in name_parts if p)
    return float(r["latitude"]), float(r["longitude"]), display

# Codici WMO -> (emoji, chiave_traduzione)
WEATHER_CODES = {
    0: ("☀️", "wmo_clear"),
    1: ("🌤️", "wmo_mainly_clear"),
    2: ("⛅", "wmo_partly_cloudy"),
    3: ("☁️", "wmo_overcast"),
    45: ("🌫️", "wmo_fog"),
    48: ("🌫️", "wmo_fog"),
    51: ("🌦️", "wmo_drizzle"),
    53: ("🌦️", "wmo_drizzle"),
    55: ("🌦️", "wmo_drizzle"),
    56: ("🌧️", "wmo_freezing_drizzle"),
    57: ("🌧️", "wmo_freezing_drizzle"),
    61: ("🌧️", "wmo_rain"),
    63: ("🌧️", "wmo_rain"),
    65: ("🌧️", "wmo_rain_heavy"),
    66: ("🌧️", "wmo_freezing_rain"),
    67: ("🌧️", "wmo_freezing_rain"),
    71: ("🌨️", "wmo_snow"),
    73: ("🌨️", "wmo_snow"),
    75: ("🌨️", "wmo_snow_heavy"),
    77: ("🌨️", "wmo_snow_grains"),
    80: ("🌧️", "wmo_showers"),
    81: ("🌧️", "wmo_showers"),
    82: ("🌧️", "wmo_showers_heavy"),
    85: ("🌨️", "wmo_snow_showers"),
    86: ("🌨️", "wmo_snow_showers"),
    95: ("⛈️", "wmo_thunder"),
    96: ("⛈️", "wmo_thunder_hail"),
    99: ("⛈️", "wmo_thunder_hail"),
}


def code_to_emoji_key(code: int) -> tuple[str, str]:
    return WEATHER_CODES.get(code, ("❓", "wmo_unknown"))


def _cache_path(lat: float, lon: float) -> Path:
    key = hashlib.sha1(f"{round(lat, 2)}|{round(lon, 2)}".encode("utf-8")).hexdigest()[:16]
    return CACHE_DIR / f"{key}.json"


def fetch_weather(lat: float, lon: float) -> tuple[dict | None, str | None]:
    """Ritorna (data, errore_o_None). data = JSON Open-Meteo (current + daily)."""
    p = _cache_path(lat, lon)
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                payload = json.load(f)
            if time.time() - payload.get("ts", 0) < CACHE_TTL:
                return payload.get("data"), None
        except (OSError, json.JSONDecodeError):
            pass

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m,precipitation",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 5,
    }
    try:
        resp = requests.get(ENDPOINT, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError) as e:
        return None, str(e)

    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"ts": time.time(), "data": data}, f, ensure_ascii=False)
    except OSError:
        pass

    return data, None
