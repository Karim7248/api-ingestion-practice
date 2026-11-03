import os
import pytest
import requests
from unittest.mock import patch

# Import the main function and the specific error we expect to catch
from main import main
from validator import ValidationError

# 1. Test Success -> returns 0
@patch("main.fetch_todo")
@patch("main.validate_todo")
def test_main_success(mock_validate, mock_fetch, tmp_path):
    # Tell our fake functions what to return
    mock_fetch.return_value = {"dummy": "data"}
    mock_validate.return_value = {"dummy": "clean_data"}
    
    # Use pytest's built-in tmp_path to create a safe, temporary folder
    test_output = tmp_path / "test.json"
    
    # Patch the variable directly inside the main module
    with patch("main.OUTPUT_PATH", str(test_output)):
        exit_code = main()
        
    assert exit_code == 0
    assert test_output.exists() # Verify the file was actually created

# 2. Test API Failure -> returns 1
@patch("main.fetch_todo")
def test_main_api_failure(mock_fetch):
    # Force the fake API client to crash with a network error
    mock_fetch.side_effect = requests.exceptions.RequestException("API is down")
    
    exit_code = main()
    
    assert exit_code == 1

# 3. Test Invalid Data -> returns 1
@patch("main.fetch_todo")
@patch("main.validate_todo")
def test_main_validation_failure(mock_validate, mock_fetch):
    # Simulate the API returning data, but the validator rejecting it
    mock_fetch.return_value = {"bad": "data"}
    mock_validate.side_effect = ValidationError("Missing required fields")
    
    exit_code = main()
    
    assert exit_code == 1