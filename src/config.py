from __future__ import annotations

import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Final, Optional

from google import genai
from google.genai.errors import APIError

from pydantic import (
    BaseModel,
    ConfigDict,
    SecretStr,
    ValidationError,
    field_validator,
    model_validator,
)

_ENV_PATH: Final[Path] = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)


class BotConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    token: SecretStr

    @field_validator("token")
    @classmethod
    def _token_not_blank(cls, value: SecretStr) -> SecretStr:
        secret = value.get_secret_value().strip()
        if not secret:
            raise ValueError("BOT_TOKEN must NOT be empty!")
        return value


class AIConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: SecretStr

    @field_validator("key")
    @classmethod
    def _key_not_blank(cls, value: SecretStr) -> SecretStr:
        secret = value.get_secret_value().strip()
        if not secret:
            raise ValueError("AI_KEY must NOT be empty!")
        return value

    @model_validator(mode="after")
    def _verify_api_key_works(self) -> AIConfig:
        raw_key = self.key.get_secret_value()
        try:
            client = genai.Client(api_key=raw_key)
            next(iter(client.models.list()))
        except APIError as err:
            raise ValueError(f"AI_KEY verification failed: Invalid key or authentication error -> {err}") from err
        except Exception as err:
            raise ValueError(f"AI_KEY verification failed: {err}") from err

        return self


class WeatherConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    api_key: Optional[SecretStr] = None

    @field_validator("api_key")
    @classmethod
    def _api_key_not_blank(cls, value: Optional[SecretStr]) -> Optional[SecretStr]:
        if value is None:
            return value
        secret = value.get_secret_value().strip()
        if not secret:
            raise ValueError("WEATHER_KEY must NOT be empty if provided!")
        return value


class Config(BaseModel):
    model_config = ConfigDict(frozen=True)

    bot: BotConfig
    ai: AIConfig
    weather: WeatherConfig

    @classmethod
    def load(cls) -> Config:
        raw_weather_key = os.getenv("WEATHER_KEY", "").strip()
        weather_secret = SecretStr(raw_weather_key) if raw_weather_key else None

        try:
            return cls(
                bot=BotConfig(token=SecretStr(os.getenv("BOT_TOKEN", ""))),
                ai=AIConfig(key=SecretStr(os.getenv("AI_KEY", ""))),
                weather=WeatherConfig(api_key=weather_secret),
            )
        except ValidationError as exc:
            raise RuntimeError(f"Invalid configuration:\n{exc}") from exc
        except ValueError as exc:
            raise RuntimeError(f"Invalid configuration: {exc}") from exc


config: Final[Config] = Config.load()