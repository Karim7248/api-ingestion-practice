import logging
import requests
from typing import Any, Dict

logger = logging.getLogger(__name__)

def fetch_todo(url: str) -> Dict[str, Any]:
    """
    Makes a GET request to the provided URL and returns the parsed JSON.
    """
    logger.info(f"Starting request to {url}")
    
    try:
        # We set an explicit timeout of 5 seconds to prevent hanging infinitely
        response = requests.get(url, timeout=5.0)
        
        # This automatically checks for bad HTTP codes (like 404 Not Found or 500 Internal Server Error)
        response.raise_for_status()
        
    except requests.exceptions.Timeout as e:
        logger.error(f"Network failure: The request to {url} timed out.")
        raise e
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP failure: The server returned an error code. Details: {e}")
        raise e
    except requests.exceptions.RequestException as e:
        logger.error(f"Network failure: A connection error occurred. Details: {e}")
        raise e

    logger.info("Successfully received response from the API.")
    
    # Parse and return the response body as a JSON dictionary
    return response.json()