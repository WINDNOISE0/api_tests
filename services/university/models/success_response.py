from pydantic import BaseModel

class SuccessResponse(BaseModel):
    details: str
    