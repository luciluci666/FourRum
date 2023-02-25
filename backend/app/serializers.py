from pydantic import BaseModel
from typing import Union
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    online: bool
    reg_time: Union[datetime, None] = None
    last_log_in_time: Union[datetime, None] = None


class Password(User):
    hashed_password: str
