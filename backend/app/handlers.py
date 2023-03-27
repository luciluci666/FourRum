from datetime import datetime
from fastapi import APIRouter, Request, Depends, Header

from app.database import User, Room, User__Room
from app.schemas import UserResponse, RoomResponse, User__RoomResponse
from app.schemas import UsersResponse, RoomsResponse, User__RoomsResponse
from app.schemas import Token, BasicResponse, RegResponse
from app.schemas import RegForm, LogInForm, CreateRoomForm, EditRoomForm, IdRoomForm

from app.utils.exceptions import SuccessefulResponse, ForbiddenException
from app.utils.auth import authenticate_user, create_access_token, get_password_hash, check_reg_data_correct, verify_email, get_user_by_jwt
from app.utils.room_helpers import check_manage_room_data_correct, get_room_by_id, edit_room, check_room_can_be_closed, check_if_user_created_room, get_not_deleted_user_rooms
from app.utils.room_helpers import delete_all_room_relationships, get_user_room_relationship, check_user_can_enter_room
from app.utils.general import get_session, object_to_json, get_all_json_of_objects_of_class, delete_object


class Handlers:

    def __init__(self, engine, debug):
        self.debug = debug
        self.router = APIRouter()
        self.engine = engine

        # debug routes
        self.router.add_api_route("/users", self.get_all_users, methods=["GET"], response_model=UsersResponse)
        self.router.add_api_route("/rooms", self.get_all_rooms, methods=["GET"], response_model=RoomsResponse)
        self.router.add_api_route("/user__rooms", self.get_all_user_room_realtionships, methods=["GET"], response_model=User__RoomsResponse)
        self.router.add_api_route("/", self.check_connection, methods=["GET"], response_model=BasicResponse)

        # authorization routes
        self.router.add_api_route("/reg", self.registration, methods=["POST"], response_model=RegResponse)
        self.router.add_api_route("/login", self.log_in_for_access_token, methods=["POST"], response_model=Token)

        # online routes (are working only with access token after logging in)

        # account routes
        self.router.add_api_route("/user/delete", self.user_delete_account, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/account", self.user_get_my_account_info, methods=["GET"], response_model=UserResponse)

        # room routes
        self.router.add_api_route("/user/room/", self.user_get_room_info, methods=["GET"], response_model=RoomResponse)
        self.router.add_api_route("/user/rooms/", self.user_get_rooms, methods=["GET"], response_model=RoomsResponse)

        self.router.add_api_route("/user/room/create", self.user_create_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/edit", self.user_edit_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/close", self.user_close_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/delete", self.user_delete_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/enter", self.user_enter_room, methods=["POST"], response_model=RoomResponse)
        self.router.add_api_route("/user/room/leave", self.user_leave_room, methods=["POST"], response_model=BasicResponse)

    # debug requests  
    async def get_all_users(self):
        if self.debug:
            session = get_session(self.engine)
            json = get_all_json_of_objects_of_class(session, User, key_name="users")
            print(json)
            return json
        else:
            raise ForbiddenException().exception
    
    async def get_all_rooms(self):
        if self.debug:
            session = get_session(self.engine)
            json = get_all_json_of_objects_of_class(session, Room, key_name="rooms")
            print(json)
            return json
        else:
            raise ForbiddenException().exception
    
    async def get_all_user_room_realtionships(self):
        if self.debug:
            session = get_session(self.engine)
            json = get_all_json_of_objects_of_class(session, User__Room, key_name="user_room_relationships")
            print(json)
            return json
        else:
            raise ForbiddenException().exception
    
    async def check_connection(self):
        return {"detail": "Connection OK", "status_code": 200}
    
    # authorization requests
    async def registration(self, data: RegForm, request: Request):
        session = get_session(self.engine)
        check_reg_data_correct(session, data)
        verify_email(data.email)
        hashed_password = get_password_hash(data.password)
        session.add(User(data.username, data.email, hashed_password, online=False, regAt=datetime.utcnow(), locale=data.locale, ip=request.client.host))
        session.commit()
        return {"detail": "Successefuly registered new account", 'reg_data': data}

    async def log_in_for_access_token(self, data: LogInForm, request: Request):
        session = get_session(self.engine)
        user = authenticate_user(session, str(data.username), str(data.password))
        access_token = create_access_token(user)
        user.jwt = access_token
        user.lastActiveAt = datetime.utcnow()
        user.ip = request.client.host
        session.commit()
        return {"access_token": user.jwt, "token_type": "bearer"}
    
    # online requests

    # account requests
    async def user_delete_account(self, token: str = Header(title="Authorization")):
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)
        delete_object(session, user)
        session.commit()
        return SuccessefulResponse("Account successefuly deleted").json
    
    async def user_get_my_account_info(self, token: str = Header(title="Authorization")):
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)
        user = object_to_json(user)
        return {"user": user}
    
    # room requests  
    async def user_get_room_info(self, room_id: int = Header(title="Room-Id"), token: str = Header(title="Authorization")):
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)
        room = get_room_by_id(session, room_id)
        get_user_room_relationship(session, user.id, room.id)
        room = object_to_json(room)
        return {"room": room}
    
    async def user_get_rooms(self, token: str = Header(title="Authorization")):
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)
        rooms = get_not_deleted_user_rooms(session, user.id)
        return rooms

    async def user_create_room(self, data: CreateRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        check_manage_room_data_correct(data, create=True)
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)
        room = Room(data.title, data.description, data.type, data.colour, creatorId=user.id, createdAt=datetime.utcnow(), isPrivate=data.isPrivate)
        session.add(room)
        session.commit()
        session.add(User__Room(user.id, room.id, userJoinedAt=datetime.utcnow(), hasAdminRights=True))
        session.commit()
        return SuccessefulResponse("Room successefuly created").json  
    
    async def user_edit_room(self, data: EditRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        check_manage_room_data_correct(data)
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)
        room = get_room_by_id(session, data.roomId)
        get_user_room_relationship(session, user.id, room.id, should_have_admin_rights=True)
        edit_room(room, data)
        session.commit()
        return SuccessefulResponse("Room successefuly edited").json

    async def user_close_room(self, data: IdRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)
        room = get_room_by_id(session, data.roomId)
        check_room_can_be_closed(room)
        check_if_user_created_room(session, user, room)
        room.isClosed = True
        session.commit()
        return SuccessefulResponse("Room successefuly closed").json 
    
    async def user_delete_room(self, data: IdRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)
        room = get_room_by_id(session, data.roomId)
        check_if_user_created_room(user, room)
        delete_object(session, room)
        delete_all_room_relationships(session, room.id)
        session.commit()
        return SuccessefulResponse("Room successefuly deleted").json 
    
    async def user_enter_room(self, data: IdRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)
        room = get_room_by_id(session, data.roomId, should_be_public=True)
        check_user_can_enter_room(session, user.id, room.id)
        session.add(User__Room(user.id, room.id, userJoinedAt=datetime.utcnow()))
        session.commit()
        room = object_to_json(room)
        return {"room": room}
    
    async def user_leave_room(self, data: IdRoomForm, token: str = Header(title="Authorization")): # TODO: when last admin leaves the admin rights are passed to the other person 
        if self.debug:                                                                             # or if there is no one else the room becomes deleted 
            print(data)
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)
        room = get_room_by_id(session, data.roomId, should_be_public=True)
        user_room_relationship = get_user_room_relationship(session, user.id, room.id)
        user_room_relationship.isDeleted = True
        session.commit()
        return SuccessefulResponse("Successefuly left the room").json 
