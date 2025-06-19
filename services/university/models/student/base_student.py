from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr

class DegreeEnumStr(StrEnum):
    ASSOCIATE = "Associate"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    DOCTORATE = "Doctorate"


class BaseStudent(BaseModel):
    model_config = ConfigDict(extra="forbid")  # запрещаем использовать лишние поля

    first_name: str
    last_name: str
    email: EmailStr
    degree: DegreeEnumStr
    phone: str
    group_id: int