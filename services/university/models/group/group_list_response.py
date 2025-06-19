from typing import List

from pydantic import BaseModel

from services.university.models.group.group_response import GroupResponse


class GroupListResponse(BaseModel):
    groups: List[GroupResponse]
