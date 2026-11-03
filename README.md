# API Ingestion Practice

A robust Python program that fetches task records from an external REST API, validates the JSON payload, and saves the clean data locally. Built as an exercise in safe network handling, data validation, and unit testing.

## Features

* **Network Resilience:** Uses explicit timeouts and HTTP status checking to prevent hanging requests and handle server errors.
* **Strict Validation:** Ensures the incoming JSON contains all required fields and correct data types before processing.
* **Separation of Concerns:** Network logic, data validation, and execution are split into distinct modules.
* **Comprehensive Logging:** Tracks request lifecycle, network failures, and validation errors without crashing silently.
* **Unit Testing:** Includes a `pytest` suite to verify validation logic locally without making live API calls.

## Project Structure

```text
api-ingestion-practice/
├── api_client.py       # Handles the HTTP GET request and network errors
├── validator.py        # Validates JSON schema and types
├── main.py             # Orchestrates the script and handles file saving
├── test_validator.py   # Pytest suite for the validation logic
└── output/             # Auto-generated folder where clean JSON is saved
```

## Requirements

* Python 3.9+
* `requests`
* `pytest`

## Installation & Usage

1. **Install dependencies:**
   ```bash
   pip install requests pytest
   ```

2. **Run the ingestion script:**
   ```bash
   python main.py
   ```
   *Check the console for logs. Upon success, the validated data will be saved to `output/todo.json`.*

3. **Run the test suite:**
   ```bash
   pytest
   ```



## Continuous Integration
* **When it runs:** Automatically triggers on every push and pull request to the `main` branch.
* **What it checks:** It provisions a fresh Ubuntu server, installs all dependencies from `requirements.txt`, and runs the `pytest` suite.
* **Why mocked tests are used:** Mocking the external API ensures the CI pipeline is fast, deterministic, and immune to network issues or third-party outages.
* **What a failure means:** A red run indicates either broken code, missing dependencies, or a failed test, which prevents unsafe code from being merged.

## Docker Integration

### Local Usage
To build and run the service locally without installing Python dependencies:
```bash
docker build -t api-ingestion:p2-8 .
docker run api-ingestion:p2-8

Configuration and Execution

Environment Variables: Set TODO_API_URL to override the target endpoint, and OUTPUT_PATH to change the save location.

Python Execution: Run OUTPUT_PATH=custom/path.json python3 main.py.

Docker Execution: Run docker run -e OUTPUT_PATH=custom/path.json api-ingestion:p2-8.

Testing: Run python3 -m pytest to execute the mocked test suite.

CI Pipeline: GitHub Actions automatically verifies pytest execution and Docker build success on every push.