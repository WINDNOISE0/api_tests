from typing import Union
from pydantic import BaseModel, ConfigDict


class DetailErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")  # запрещаем использовать лишние поля

    loc: list[Union[str, int]]
    msg: str
    type: str
