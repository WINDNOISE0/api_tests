from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid") # запрещаем использовать лишние поля

    username: str
    password: str