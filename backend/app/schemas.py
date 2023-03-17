from pydantic import BaseModel
from typing import Union
from datetime import date, time


class Token(BaseModel):
    access_token: str
    token_type: str

class RegUser(BaseModel):
    username: str
    email: str
    password: str
    locale: str

class LogInUser(BaseModel):
    username: str
    password: str

class BasicResponse(BaseModel):
    detail: str
    status: int

class RegResponse(BaseModel):
    detail: str
    reg_data: RegUser

class UserJson(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    online: bool
    reg_date: Union[date, None] = None
    last_log_in_date: Union[time, None] = None
    last_log_in_time: Union[time, None] = None
    jwt: Union[str, None] = None