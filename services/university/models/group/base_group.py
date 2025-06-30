from pydantic import BaseModel, ConfigDict


class BaseGroup(BaseModel):
    model_config = ConfigDict(extra="forbid")  # запрещаем использовать лишние поля

    name: str

