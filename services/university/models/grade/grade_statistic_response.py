from pydantic import BaseModel, field_validator


class GradeStatisticResponse(BaseModel):
    count: int
    min: int
    max: int
    avg: float

    @field_validator("avg")
    def validate_avg_more_zero(cls, value):
        if value < 0:
            raise ValueError("avg must be greater than zero")
