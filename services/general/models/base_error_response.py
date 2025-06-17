from pydantic import BaseModel, ConfigDict

from services.general.models.detail_error_response import DetailErrorResponse


class BaseErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")  # запрещаем использовать лишние поля

    detail: list[DetailErrorResponse]