from typing import List

from pydantic import BaseModel

from services.university.models.error.validation_error import ValidationError


class ValidationErrorList(BaseModel):
    detail: List[ValidationError]
