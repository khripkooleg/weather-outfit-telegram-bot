from __future__ import annotations

import asyncio
import datetime
import logging
from typing import Final

from src.weather.connect import openmeteo_client
from src.weather.schemas import DailyWeather

logger = logging.getLogger(__name__)

OPEN_METEO_URL: Final[str] = "https://api.open-meteo.com/v1/forecast"


def _fetch_sync_weather(lat: float, lon: float) -> DailyWeather:
    today_str = datetime.date.today().isoformat()

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "timezone": "auto",
        "start_date": today_str,
        "end_date": today_str,
    }

    responses = openmeteo_client.weather_api(OPEN_METEO_URL, params=params)
    response = responses[0]

    daily = response.Daily()
    if daily is None:
        raise ValueError("No daily weather data returned from Open-Meteo API.")

    var_max = daily.Variables(0)
    var_min = daily.Variables(1)

    if var_max is None or var_min is None:
        raise ValueError("Missing daily temperature variables in Open-Meteo response.")

    daily_temp_max = var_max.ValuesAsNumpy()
    daily_temp_min = var_min.ValuesAsNumpy()

    temp_max = round(float(daily_temp_max[0]), 1)
    temp_min = round(float(daily_temp_min[0]), 1)
    temp_avg = round((temp_max + temp_min) / 2, 1)

    return DailyWeather(
        temp_min=temp_min,
        temp_max=temp_max,
        temp_avg=temp_avg,
    )


async def get_today_weather(lat: float = 49.2331, lon: float = 28.4682) -> DailyWeather:
    try:
        return await asyncio.to_thread(_fetch_sync_weather, lat, lon)
    except Exception as err:
        logger.error(f"Failed to fetch weather data: {err}")
        raise