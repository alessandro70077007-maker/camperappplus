"""Fetch aree sosta camper / camper service da OpenStreetMap via Overpass API.
Cache 24h su file JSON per rispettare i rate limit Overpass."""
import hashlib
import json
import math
import time
from pathlib import Path

import requests

import storage


CACHE_TTL = 24 * 3600  # 24h
CACHE_DIR = storage.DATA_DIR / "poi_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Endpoint Overpass: il principale + un mirror come fallback
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

# Tipi di POI supportati: chiave -> (overpass_filter, label_key, color)
POI_TYPES = {
    "caravan_site": ("tourism=caravan_site", "poi_caravan_site", "#1f77b4"),
    "sanitary_dump": ("amenity=sanitary_dump_station", "poi_sanitary_dump", "#2ca02c"),
    "camp_site": ("tourism=camp_site", "poi_camp_site", "#d62728"),
}


def _cache_key(lat: float, lon: float, radius_km: int, types: tuple) -> str:
    # arrotonda lat/lon a 0.01° (~1km) per riusare cache su posizioni vicine
    payload = f"{round(lat, 2)}|{round(lon, 2)}|{radius_km}|{','.join(sorted(types))}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]


def _cache_path(key: str) -> Path:
    return CACHE_DIR / f"{key}.json"


def _load_from_cache(key: str):
    p = _cache_path(key)
    if not p.exists():
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            payload = json.load(f)
        if time.time() - payload.get("ts", 0) > CACHE_TTL:
            return None
        return payload.get("results")
    except (OSError, json.JSONDecodeError):
        return None


def _save_to_cache(key: str, results: list) -> None:
    try:
        with open(_cache_path(key), "w", encoding="utf-8") as f:
            json.dump({"ts": time.time(), "results": results}, f, ensure_ascii=False)
    except OSError:
        pass


def _build_query(lat: float, lon: float, radius_m: int, types: tuple) -> str:
    parts = []
    for t in types:
        if t in POI_TYPES:
            tag = POI_TYPES[t][0]
            k, v = tag.split("=", 1)
            for kind in ("node", "way", "relation"):
                parts.append(f'{kind}["{k}"="{v}"](around:{radius_m},{lat},{lon});')
    body = "\n".join(parts)
    return f"[out:json][timeout:25];(\n{body}\n);out center tags;"


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _normalize_element(el: dict, my_lat: float, my_lon: float) -> dict | None:
    """Estrae lat/lon, nome e tipo da un elemento Overpass."""
    if el.get("type") == "node":
        lat, lon = el.get("lat"), el.get("lon")
    else:
        center = el.get("center") or {}
        lat, lon = center.get("lat"), center.get("lon")
    if lat is None or lon is None:
        return None
    tags = el.get("tags") or {}
    # determina il tipo dal tag
    poi_type = None
    if tags.get("tourism") == "caravan_site":
        poi_type = "caravan_site"
    elif tags.get("amenity") == "sanitary_dump_station":
        poi_type = "sanitary_dump"
    elif tags.get("tourism") == "camp_site":
        poi_type = "camp_site"
    return {
        "id": el.get("id"),
        "type": poi_type,
        "name": tags.get("name") or "",
        "lat": float(lat),
        "lon": float(lon),
        "distance_km": round(haversine_km(my_lat, my_lon, float(lat), float(lon)), 2),
        "operator": tags.get("operator", ""),
        "website": tags.get("website") or tags.get("contact:website") or "",
        "phone": tags.get("phone") or tags.get("contact:phone") or "",
        "fee": tags.get("fee", ""),
    }


def fetch_pois(lat: float, lon: float, radius_km: int, types: tuple) -> tuple[list, str | None]:
    """Ritorna (results, errore_o_None). results = lista di dict normalizzati,
    ordinati per distanza. Usa la cache se valida."""
    if not types:
        return [], None
    key = _cache_key(lat, lon, radius_km, types)
    cached = _load_from_cache(key)
    if cached is not None:
        return cached, None

    query = _build_query(lat, lon, radius_km * 1000, types)
    last_err = None
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            resp = requests.post(endpoint, data={"data": query}, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            elements = data.get("elements", [])
            results = []
            seen_ids = set()
            for el in elements:
                norm = _normalize_element(el, lat, lon)
                if norm is None:
                    continue
                # dedup per id (way + relation possono duplicare)
                if norm["id"] in seen_ids:
                    continue
                seen_ids.add(norm["id"])
                results.append(norm)
            results.sort(key=lambda x: x["distance_km"])
            _save_to_cache(key, results)
            return results, None
        except (requests.RequestException, ValueError) as e:
            last_err = str(e)
            continue
    return [], last_err or "unknown error"
