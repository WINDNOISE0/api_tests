from pydantic import Field

from pydantic import BaseModel, field_validator


class GradeStatisticResponse(BaseModel):
    count: int
    min: int
    max: int
    avg: float = Field(ge=0, description="Average must be ≥ 0")
