from __future__ import annotations

import openmeteo_requests
import requests_cache
from retry_requests import retry

_cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
_retry_session = retry(_cache_session, retries=5, backoff_factor=0.2)

openmeteo_client = openmeteo_requests.Client(session=_retry_session) # type: ignore[arg-type]