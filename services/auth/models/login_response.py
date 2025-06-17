from typing import Literal

from pydantic import BaseModel, ConfigDict


class LoginResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")  # запрещаем использовать лишние поля

    access_token: str
    token_type: Literal["Bearer"]
