from enum import StrEnum

from pydantic import BaseModel

class SubjectEnumStr(StrEnum):
    MATHEMATICS = "Mathematics"
    PHYSICS = "Physics"
    HISTORY = "History"
    BIOLOGY = "Biology"
    GEOGRAPHY = "Geography"


class BaseTeacher(BaseModel):
    first_name: str
    last_name: str
    subject: SubjectEnumStr


