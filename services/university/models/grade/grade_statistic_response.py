from pydantic import Field

from pydantic import BaseModel


class GradeStatisticResponse(BaseModel):
    count: int
    min: int
    max: int
    avg: float = Field(ge=0)
