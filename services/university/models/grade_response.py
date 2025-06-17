from pydantic import field_validator

from services.university.models.grade_base import GradeBase

class GradeResponse(GradeBase):
    id: int
    grade: int

    @field_validator("grade")
    def validate_grade_range(cls, value):
        if value not in range(1, 6):
            raise ValueError("Grade must be in range [1-2-3-4-5].")
        return value


