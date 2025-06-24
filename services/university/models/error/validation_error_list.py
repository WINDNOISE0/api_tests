from pydantic import BaseModel

from services.university.models.error.validation_error import ValidationError


class ValidationErrorList(BaseModel):
    detail: list[ValidationError]
