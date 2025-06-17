from typing import Union

from services.university.models.grade_base import GradeBase


class GradeRequest(GradeBase):
    group_id: int