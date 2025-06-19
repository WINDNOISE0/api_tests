from typing import Literal

from pydantic import BaseModel


class ConflictResponse(BaseModel):
    detail: Literal["Group is already created"]
