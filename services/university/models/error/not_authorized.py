from typing import Literal

from pydantic import BaseModel


class NotAuthorized(BaseModel):
    detail: Literal["Invalid login credentials"]
