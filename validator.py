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

    required_fields = ["userId", "id", "title", "completed"]

    for field in required_fields:
        if field not in data:
            logger.error(f"Vlidation failed: Missing required field '{field}' ")
            raise ValidationError(f"Missing required field: {field}")

    if not isinstance(data["completed"], bool):
        logger.error(f"Validation failed: 'completed' field must be a boolean")
        raise ValidationError("'completed field must be a boolean" )

    if not isinstance(data["userId"], int):
            logger.error(f"Validation failed: 'userId' field must be a integer")
            raise ValidationError(" userId field must be a integer" )

    if not isinstance(data["id"], int):
            logger.error(f"Validation failed: 'id' field must be a integer")
            raise ValidationError("id field must be a integer" )

    if not isinstance(data["title"], str):
            logger.error(f"Validation failed: 'title' field must be a string")
            raise ValidationError("title field must be a string" )
    

    logger.info("JSON payload successfully validated.")
    return data