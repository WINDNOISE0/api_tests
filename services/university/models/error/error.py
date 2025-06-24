from enum import StrEnum

from pydantic import BaseModel


class Error(BaseModel):
    detail: str


class ErrorText(StrEnum):
    FORBIDDEN = "Invalid JWT token"
    NO_AUTH = "Access denied"
    CONFLICT_RESPONSE = "Group is already created"
