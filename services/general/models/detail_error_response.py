from pydantic import BaseModel, ConfigDict


class DetailErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")  # запрещаем использовать лишние поля

    loc: list[str | int]
    msg: str
    type: str
