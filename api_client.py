import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


def fetch_todo(url: str, timeout: float = 5.0) -> dict[str, Any]:
    """Fetch a todo JSON object from an HTTP endpoint.

    Network-related exceptions are logged and re-raised so the caller can
    decide how the application should handle the failure.
    """
    logger.info("Starting request to %s", url)

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout as e:
        logger.error("Request to %s timed out: %s", url, e)
        raise
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error while requesting %s: %s", url, e)
        raise
    except requests.exceptions.RequestException as e:
        logger.error("Request to %s failed: %s", url, e)
        raise

    logger.info("Successfully received response from the API.")
    return response.json()
