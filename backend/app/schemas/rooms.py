from pydantic import BaseModel
from typing import Union, List
from datetime import datetime


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

class RoomsResponse(BaseModel):
    rooms: List[RoomModel]

class User__RoomsResponse(BaseModel):
    user_room_relationships: List[User__RoomModel]

class RoomResponse(BaseModel):
    room: RoomModel

class User__RoomResponse(BaseModel):
    user_room_relationship: User__RoomModel