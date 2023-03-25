from fastapi import HTTPException, status
from re import match
from app.database import Room, User__Room
from app.schemas import CreateRoomForm, EditRoomForm
from app.utils.exceptions import ValidationException

hex_format =  r"^#?([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})$"

def check_manage_room_data_correct(data: EditRoomForm, create=False):
    if (not data.title) or (not data.description) or (not data.access) or (not data.colour):
        raise ValidationException("All keys can't be empty").exception
    elif len(data.title) > 32 or len(data.description) > 128:
        raise ValidationException("Title must be 32 or less letters and description must be 128 or less letters long").exception
    elif not (data.access == "public" or data.access == "private"):
        raise ValidationException("Invalid access key: it can be only 'public' or 'private'").exception
    elif not match(hex_format, data.colour):
        raise ValidationException("Invalid colour key: it must be in hex format").exception
    elif create:
        if not data.type:
            raise ValidationException("Type key can't be empty").exception
        if not (data.type == "group" or data.type == "channel" or data.type == "thread" or data.type == "discussion"):
            raise ValidationException("Invalid type key: by this time room can be only 4 types: 'group', 'channel', 'thread', 'discussion'").exception

def get_room_by_id(session, room_id, should_be_public=False):
    room = session.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The room you are trying to access can not be found"
        )
    elif room.isDeleted:
        raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="The room you are trying to access was deleted"
        )
    elif should_be_public:
        if room.access == "private":
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This room is private"
            )
    return room

def edit_room(room, edit_data):
    room.title = edit_data.title
    room.description = edit_data.description
    room.access = edit_data.access
    room.colour = edit_data.colour

def check_room_can_be_closed(room):
    if not (room.type == "thread" or room.type == "discussion"):
        raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Room of this type can not be closed"
        )

def check_if_user_created_room(user, room):
    if not room.creatorId == user.id:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not a creator of this room"
        )
    
def get_user_room_relationship(session, user_id, room_id, should_have_admin_rights=False):
    user_room_relationship = session.query(User__Room).filter(User__Room.userId == user_id, User__Room.roomId == room_id).order_by(User__Room.id.desc()).first()
    if not user_room_relationship:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not a member of this room"
        )
    elif user_room_relationship.isDeleted:
        raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="You are not a member of this room anymore"
        )
    elif should_have_admin_rights:
        if not user_room_relationship.hasAdminRights:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have admin rights in this room"
            )
    return user_room_relationship
    
def check_user_room_relationship(session, user_id, room_id):
    user_room_relationship = session.query(User__Room).filter(User__Room.userId == user_id).filter(User__Room.roomId == room_id).order_by(User__Room.id.desc()).first()
    if user_room_relationship:
        if not user_room_relationship.isDeleted:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already are a member of this room"
                )
        if user_room_relationship.userWasKicked:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You were kicked from this room"
                )
        
def get_not_deleted_rooms(session, user_id):
    user__rooms = session.query(User__Room).filter(User__Room.userId == user_id)
    rooms = []
    for user__room in user__rooms:
        new_room = session.query(Room).filter(Room.id == user__room.roomId).first()
        if new_room:
            if not new_room.isDeleted:
                rooms.append(new_room)
    return rooms

