from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class DailyWeather:
    temp_min: float
    temp_max: float
    temp_avg: float