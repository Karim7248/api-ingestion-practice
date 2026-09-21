import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class ValidationError(ValueError):
    """Custom exception for when the incoming JSON does not meet our schema."""
    pass

def validate_todo(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates that the incoming JSON has the correct fields and types.
    Raises ValidationError if validation fails.
    """

    required_fields = ["user_Id", "id", "title", "completed"]

    for field in required_fields:
        if field not in data:
            logger.error(f"Vlidation failed: Missing required field '{field}' ")
            raise ValidationError(f"Missing required field: {field}")

    if not isinstance(data["completed"], bool):
        logger.error(f"Validation failed: 'completed' field must be a boolean")
        raise ValidationError("'completed field must be a boolean" )

    logger.info("JSON payload successfully validated.")
    return data