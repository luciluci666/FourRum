from pydantic import BaseModel
from typing import Union, List
from datetime import datetime


class UserModel(BaseModel):
    id: int
    username: str
    email: str
    hashedPassword: str
    online: bool
    regAt: datetime 
    ip: str
    locale: str
    lastActiveAt: Union[datetime, None] = None
    jwt: Union[str, None] = None
    isDeleted: bool
    deletedAt: Union[datetime, None] = None

class UserResponse(BaseModel):
    user: UserModel

class UsersResponse(BaseModel):
    users: List[UserModel]
    