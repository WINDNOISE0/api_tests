from typing import List

from pydantic import BaseModel

from services.university.models.grade.grade_response import GradeResponse


class GradeListResponse(BaseModel):
    grades: List[GradeResponse]
