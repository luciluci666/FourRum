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

class RoomModel(BaseModel):
    id: int
    title: str
    description: str  
    type: str 
    isPrivate: bool
    colour: str
    creatorId: int  
    createdAt: datetime
    isClosed: bool
    isDeleted: bool
    deletedAt: Union[datetime, None] = None

class User__RoomModel(BaseModel):
    id: int
    userId: int
    roomId: int
    userJoinedAt: datetime
    hasAdminRights: bool
    userWasKicked: bool
    isDeleted: bool
    deletedAt: Union[datetime, None] = None

class RegForm(BaseModel):
    username: str
    email: str
    password: str
    locale: str

class LogInForm(BaseModel):
    username: str
    password: str

class CreateRoomForm(BaseModel):
    title: str
    description: str
    type: str
    isPrivate: bool
    colour: str

class EditRoomForm(BaseModel):
    roomId: int
    title: str
    description: str
    isPrivate: bool
    colour: str

class IdRoomForm(BaseModel):
    roomId: int


class Token(BaseModel):
    access_token: str
    token_type: str

class BasicResponse(BaseModel):
    detail: str
    status_code: int

class RegResponse(BaseModel):
    detail: str
    reg_data: RegForm

class UsersResponse(BaseModel):
    users: List[UserModel]

class RoomsResponse(BaseModel):
    rooms: List[RoomModel]

class User__RoomsResponse(BaseModel):
    user_room_relationships: List[User__RoomModel]