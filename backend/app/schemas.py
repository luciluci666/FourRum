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

class UsersResponse(BaseModel):
    users: List[UserModel]

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

class Room(BaseModel):
    id: int
    title: str
    description: str  
    type: str 
    colour: str  
    creatorId: int  
    createdAt: datetime  

class RoomResponse(BaseModel):
    rooms: List[Room]