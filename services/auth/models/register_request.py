import re

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


MIN_LEN_PASSWORD = 8
MAX_LEN_PASSWORD = 100

class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid") # запрещаем использовать лишние поля

    username: str
    password: str
    password_repeat: str
    email: EmailStr

    @field_validator("password")
    def validate_password_strength(cls, value):
        if len(value) < MIN_LEN_PASSWORD:
            raise ValueError("Password must be longer than 7 characters.")
        if len(value) > MAX_LEN_PASSWORD:
            raise ValueError("Password must be shorter than 100 characters.")
        if not re.search(r"[!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]", value):
            raise ValueError("Password must contain at least one special character.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        return value

    @field_validator("password_repeat")
    def passwords_match(cls, repeat, values):
        original = values.data.get("password")
        if repeat != original:
            raise ValueError("Passwords do not match.")
        return repeat
