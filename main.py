import os
import json
import logging
import requests
from api_cliente import fetch_todo
from validator import validate_todo, ValidationError

# Configure the master logging settings for the whole application
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    output_dir = "output"
    output_file = os.path.join(output_dir, "todo.json")

    logger.info("Starting the ingestion process...")

    try:
        # Step 1: Call the API (our network logic)
        raw_data = fetch_todo(url)
        
        # Step 2: Validate the JSON (our validation logic)
        clean_data = validate_todo(raw_data)
        
        # Step 3: Save it locally
        # First, ensure the 'output' directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Open the file in 'write' mode and dump the JSON into it
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(clean_data, f, indent=4)
            
        logger.info(f"Successfully saved clean JSON to {output_file}")

    # Catching specific errors from our modules
    except requests.exceptions.RequestException:
        logger.error("Ingestion failed: Could not retrieve data from the API.")
        return 1
    except ValidationError:
        logger.error("Ingestion failed: The retrieved data was invalid.")
        return 1
    except OSError as e:
        logger.error(f"Ingestion failed: Could not save the file to disk. Details: {e}")
        return 1

    return 0

# This tells Python to only run main() if this file is executed directly
if __name__ == "__main__":
    raise SystemExit(main())