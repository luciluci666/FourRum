from pydantic import BaseModel


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
