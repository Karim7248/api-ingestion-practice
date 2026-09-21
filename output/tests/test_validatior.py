import pytest
from validator import validate_todo, ValidationError

def test_valid_json_passes():
    """Test that a perfectly formed dictionary is returned as-is."""
    valid_data = {
        "userId": 1,
        "id": 12,
        "title": "Hello yo"
        "completed": False
    }

    result = validate_todo(valid_data)

    assert result == valid_data

def test_missing_required_field_fails():
    """Test that a title is removed from the fields"""
    invalid_data = {
        "userId": 1,
        "id": 12,
        #"title": "Hello yo"
        "completed": False
    }

    with pytest.raises(ValidationError):
        validate_todo(invalid_data)

def test_incorrect_field_type_fails():
    """Test that a string in the 'completed' field (instead of a boolean) fails."""
    invalid_data = {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": "false"  # This is a string, not a boolean!
        }
    with pytest.raises(ValidationError):
        validate_todo(invalid_data)    