import json
import logging
import os
import sys

import requests

from api_client import fetch_todo
from validator import ValidationError, validate_todo

API_URL = os.environ.get("TODO_API_URL", "https://jsonplaceholder.typicode.com/todos/1")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "output/todo.json")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] - %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    logger.info("Starting the ingestion process...")

    try:
        raw_data = fetch_todo(API_URL)
        clean_data = validate_todo(raw_data)

        # Extract the directory path (e.g. "output") from the full file path
        output_dir = os.path.dirname(OUTPUT_PATH)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        # Use OUTPUT_PATH to write the file, not the undefined output_file variable
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(clean_data, f, indent=4)

        logger.info("Successfully saved clean JSON to %s", OUTPUT_PATH)
        
    except requests.exceptions.RequestException:
        logger.error("Ingestion failed: Could not retrieve data from the API.")
        return 1
    except ValidationError:
        logger.error("Ingestion failed: The retrieved data was invalid.")
        return 1
    except OSError as e:
        logger.error("Ingestion failed: Could not save the file to disk. Details: %s", e)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())