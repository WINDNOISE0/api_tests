from typing import Literal

from pydantic import BaseModel


class Forbidden(BaseModel):
    detail: Literal["Invalid JWT token"]
