import json
import logging
import os

import requests

from api_client import fetch_todo
from validator import ValidationError, validate_todo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    url = "https://jsonplaceholder.typicode.com/todos/1"
    output_dir = "output"
    output_file = os.path.join(output_dir, "todo.json")

    logger.info("Starting the ingestion process...")

    try:
        raw_data = fetch_todo(url)
        clean_data = validate_todo(raw_data)

        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(clean_data, f, indent=4)

        logger.info("Successfully saved clean JSON to %s", output_file)
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
