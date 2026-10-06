from __future__ import annotations

import logging
from typing import Optional

from google import genai
from google.genai import types

from src.config import config

logger = logging.getLogger(__name__)

_client: Optional[genai.Client] = None

_REQUEST_TIMEOUT_MS = 12_000

_RETRY_OPTIONS = types.HttpRetryOptions(
    attempts=3,
    initial_delay=1.0,
    max_delay=8.0,
    exp_base=2,
    http_status_codes=[429, 500, 503, 504],
)


def get_genai_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = config.ai.key.get_secret_value()
        _client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=_REQUEST_TIMEOUT_MS,
                retry_options=_RETRY_OPTIONS,
            ),
        )
        logger.info("Initialized Google GenAI Client successfully!")
    return _client


async def close_genai_client() -> None:
    global _client
    if _client is not None:
        await _client.aio.aclose()
        _client.close()
        _client = None
        logger.info("Closed Google GenAI Client connections.")


ai_client: genai.Client = get_genai_client()