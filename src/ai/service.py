from __future__ import annotations

import logging
from typing import Final

from google.genai import types
from google.genai.errors import APIError

from src.ai.connect import ai_client
from src.ai.prompt import OUTFIT_SYSTEM_INSTRUCTION, build_outfit_prompt
from src.weather.schemas import DailyWeather

logger = logging.getLogger(__name__)

_MODELS: Final[tuple[str, ...]] = (
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
)

_RETRYABLE_CODES: Final[frozenset[int]] = frozenset({429, 500, 503, 504})

_BUSY_MESSAGE: Final[str] = (
    "Служба рекомендацій зараз перевантажена, будь ласка, спробуйте ще раз через хвилину."
)

_REQUEST_HTTP_OPTIONS: Final[types.HttpOptions] = types.HttpOptions(
        timeout=10_000,
        retry_options=types.HttpRetryOptions(
        attempts=1,
        http_status_codes=list(_RETRYABLE_CODES),
    ),
)


async def generate_outfit_recommendation(
    weather: DailyWeather,
) -> str:
    prompt = build_outfit_prompt(
        temp_min=weather.temp_min,
        temp_max=weather.temp_max,
        temp_avg=weather.temp_avg,
    )

    for model in _MODELS:
        try:
            response = await ai_client.aio.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=OUTFIT_SYSTEM_INSTRUCTION,
                    temperature=0.7,
                    max_output_tokens=500,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    ),
                    http_options=_REQUEST_HTTP_OPTIONS,
                ),
            )
        except APIError as err:
            if err.code not in _RETRYABLE_CODES:
                raise
            logger.warning("Model %s unavailable (%s), trying next model", model, err.code)
            continue

        if response.text:
            return response.text

        logger.warning("Model %s returned empty text, trying next model", model)

    return _BUSY_MESSAGE