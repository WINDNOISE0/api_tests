from pydantic import BaseModel, field_validator


class GradeBase(BaseModel):
    teacher_id: int
    student_id: int
    grade: int

    @field_validator("grade")
    def validate_grade_range(cls, value):
        if value not in range(1, 6):
            raise ValueError("Grade must be in range [1-2-3-4-5].")
        return value
