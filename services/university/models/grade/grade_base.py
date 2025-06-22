from pydantic import BaseModel, field_validator

MIN_GRADE = 1
MAX_GRADE = 5


class GradeBase(BaseModel):
    teacher_id: int
    student_id: int
    grade: int

    @field_validator("grade")
    def validate_grade_range(cls, value):
        if value not in range(MIN_GRADE, MAX_GRADE + 1):
            raise ValueError(f"Grade must be in range {MIN_GRADE}-{MAX_GRADE}.")
        return value
