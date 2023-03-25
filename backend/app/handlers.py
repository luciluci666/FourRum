from datetime import datetime
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Request, Depends, Header
from json import dump

from app.schemas import Token, BasicResponse, RegResponse, UsersResponse, RoomsResponse
from app.schemas import RegForm, LogInForm, CreateRoomForm, EditRoomForm, IdRoomForm
from app.database import User, Room, User__Room

from app.utils.auth import authenticate_user, create_access_token, get_password_hash, check_reg_data_correct, verify_email, get_user_by_jwt
from app.utils.room_helpers import check_manage_room_data_correct, get_room_by_id, edit_room, check_room_can_be_closed, check_if_user_created_room, get_not_deleted_rooms
from app.utils.room_helpers import get_user_room_relationship, check_user_room_relationship
from app.utils.exceptions import SuccessefulResponse

class Handlers:

    def __init__(self, engine, debug):
        self.debug = debug
        self.router = APIRouter()
        self.engine = engine
        Session = sessionmaker(self.engine)
        self.session = Session()

        self.router.add_api_route("/user/reg/", self.registration, methods=["POST"], response_model=RegResponse)
        self.router.add_api_route("/user/login/", self.log_in_for_access_token, methods=["POST"], response_model=Token)
        self.router.add_api_route("/users", self.get_all_users, methods=["GET"], response_model=UsersResponse)
        self.router.add_api_route("/", self.check_connection, methods=["GET"], response_model=BasicResponse)

        # online routes

        # account routes
        self.router.add_api_route("/user/delete/", self.user_delete_account, methods=["POST"], response_model=BasicResponse)

        # room routes
        self.router.add_api_route("/user/room/create", self.user_create_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/edit", self.user_edit_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/close", self.user_close_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/delete", self.user_delete_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/enter", self.user_enter_room, methods=["POST"], response_model=RoomsResponse)
        self.router.add_api_route("/user/room/leave", self.user_leave_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/rooms/", self.user_get_rooms, methods=["GET"], response_model=RoomsResponse)


    async def registration(self, data: RegForm, request: Request):
        if check_reg_data_correct(self.session, data):
            if verify_email(data.email):
                hashed_password = get_password_hash(data.password)
                self.session.add(User(data.username, data.email, hashed_password, online=False, regAt=datetime.utcnow(), locale=data.locale, ip=request.client.host))
                self.session.commit()
                return {"detail": "Successefuly registered new account", 'reg_data': data}

    async def log_in_for_access_token(self, data: LogInForm, request: Request):
        user = authenticate_user(self.session, str(data.username), str(data.password))
        access_token = create_access_token(user)
        user.jwt = access_token
        user.lastActiveAt = datetime.utcnow()
        user.ip = request.client.host
        self.session.commit()
        return {"access_token": user.jwt, "token_type": "bearer"}
        
    async def get_all_users(self):
        my_json = {
            "users": []
        }
        users = self.session.query(User).all()
        for user in users:
            dict = user.__dict__
            del dict['_sa_instance_state']
            my_json["users"].append(dict)
        return my_json
    
    async def check_connection(self):
        return {"detail": "Connection OK", "status_code": 200}
    
    # online requests
    async def user_delete_account(self, token: str = Header(title="Authorization")):
        user = get_user_by_jwt(self.session, token)
        user.isDeleted = True
        self.session.commit()
        return SuccessefulResponse("Account successefuly deleted").json
    
    # room requests
    async def user_create_room(self, data: CreateRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        check_manage_room_data_correct(data, create=True)
        user = get_user_by_jwt(self.session, token)
        room = Room(data.title, data.description, data.type, data.access, data.colour, user.id, createdAt=datetime.utcnow())
        self.session.add(room)
        self.session.commit()
        self.session.add(User__Room(user.id, room.id, userJoinedAt=datetime.utcnow(), hasAdminRights=True))
        self.session.commit()
        return SuccessefulResponse("Room successefuly created").json  
    
    async def user_edit_room(self, data: EditRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        check_manage_room_data_correct(data)
        user = get_user_by_jwt(self.session, token)
        room = get_room_by_id(self.session, data.roomId)
        get_user_room_relationship(self.session, user.id, room.id, should_have_admin_rights=True)
        edit_room(self.session, room, data)
        self.session.commit()
        return SuccessefulResponse("Room successefuly edited").json

    async def user_close_room(self, data: IdRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        user = get_user_by_jwt(self.session, token)
        room = get_room_by_id(self.session, data.roomId)
        check_room_can_be_closed(room)
        check_if_user_created_room(self.session, user, room)
        room.isClosed = True
        self.session.commit()
        return SuccessefulResponse("Room successefuly closed").json 
    
    async def user_delete_room(self, data: IdRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        user = get_user_by_jwt(self.session, token)
        room = get_room_by_id(self.session, data.roomId)
        check_if_user_created_room(user, room)
        room.isDeleted = True
        self.session.commit()
        return SuccessefulResponse("Room successefuly deleted").json 
    
    async def user_enter_room(self, data: IdRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        user = get_user_by_jwt(self.session, token)
        room = get_room_by_id(self.session, data.roomId, should_be_public=True)
        print(room)
        check_user_room_relationship(self.session, user.id, room.id)
        self.session.add(User__Room(user.id, room.id, userJoinedAt=datetime.utcnow()))
        self.session.commit()
        return {"rooms": [room]}
    
    async def user_leave_room(self, data: IdRoomForm, token: str = Header(title="Authorization")):
        if self.debug:
            print(data)
        user = get_user_by_jwt(self.session, token)
        room = get_room_by_id(self.session, data.roomId, should_be_public=True)
        user_room_relationship = get_user_room_relationship(self.session, user.id, room.id)
        user_room_relationship.isDeleted = True
        self.session.commit()
        return SuccessefulResponse("Successefuly left the room").json 
    
    async def user_get_rooms(self, token: str = Header(title="Authorization")):
        user = get_user_by_jwt(self.session, token)
        rooms = get_not_deleted_rooms(self.session, user.id)
        print(rooms)
        return {"rooms": rooms}
    
