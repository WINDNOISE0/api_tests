from pydantic import BaseModel

class GradeBase(BaseModel):
    teacher_id: int
    student_id: int




