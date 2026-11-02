import pytest

from validator import ValidationError, validate_todo


def test_valid_json_passes():
    valid_data = {
        "userId": 1,
        "id": 12,
        "title": "Hello yo",
        "completed": True,
    }

    assert validate_todo(valid_data) == valid_data


def test_missing_required_field_fails():
    invalid_data = {
        "userId": 1,
        "id": 12,
        "completed": False,
    }

    with pytest.raises(ValidationError):
        validate_todo(invalid_data)


def test_incorrect_field_types_fail():
    valid_data = {
        "userId": 1,
        "id": 1,
        "title": "delectus aut autem",
        "completed": False,
    }

    invalid_values = {
        "userId": "1",
        "id": "1",
        "title": 123,
        "completed": "false",
    }

    for field, invalid_value in invalid_values.items():
        invalid_data = valid_data.copy()
        invalid_data[field] = invalid_value

        with pytest.raises(ValidationError):
            validate_todo(invalid_data)
