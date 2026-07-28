from __future__ import annotations

import logging
import time
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Short backoff for genuine transient rate limiting (requests-per-minute style
# throttling) - the kind a live demo can trip by asking a few questions in
# quick succession. It deliberately does NOT help once a hard daily quota is
# actually exhausted; that case is handled by the caller falling back to a
# degraded response, not by retrying blindly.
RETRY_DELAYS_SECONDS: tuple[float, ...] = (1.5, 3.0)


def is_rate_limited(exc: Exception) -> bool:
    message = str(exc)
    return "RESOURCE_EXHAUSTED" in message or "429" in message or "quota" in message.lower()


def call_with_retry(fn: Callable[[], T]) -> T:
    """
    Run a synchronous Gemini SDK call, retrying on transient rate limits with
    short backoff before giving up. Non-rate-limit errors and the final
    attempt's rate-limit error both propagate immediately - the caller is
    responsible for deciding what a still-failing call degrades to.
    """
    attempts = len(RETRY_DELAYS_SECONDS) + 1
    for attempt in range(attempts):
        try:
            return fn()
        except Exception as exc:
            if attempt >= attempts - 1 or not is_rate_limited(exc):
                raise
            delay = RETRY_DELAYS_SECONDS[attempt]
            logger.warning("Rate limited, retrying in %.1fs (attempt %s/%s)", delay, attempt + 1, attempts - 1)
            time.sleep(delay)
    raise AssertionError("unreachable")  # pragma: no cover
