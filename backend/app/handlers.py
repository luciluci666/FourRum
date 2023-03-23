from datetime import datetime
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Request, Depends, Header
from fastapi.security import OAuth2PasswordBearer

from app.schemas import Token, RegUser, LogInUser, BasicResponse, RegResponse, UsersResponse, RoomResponse
from app.database import User, Room, User__Room
from .utils import authenticate_user, create_access_token, get_password_hash, check_reg_data_correct, verify_email, get_user_by_jwt


class Handlers:

    def __init__(self, engine):
        self.router = APIRouter()
        self.engine = engine
        Session = sessionmaker(self.engine)
        self.session = Session()

        self.router.add_api_route("/user/reg/", self.registration, methods=["POST"], response_model=RegResponse)
        self.router.add_api_route("/user/login/", self.log_in_for_access_token, methods=["POST"], response_model=Token)
        self.router.add_api_route("/users", self.get_all_users, methods=["GET"], response_model=UsersResponse)
        self.router.add_api_route("/", self.check_connection, methods=["GET"], response_model=BasicResponse)

        # online routes
        self.router.add_api_route("/user/delete/", self.delete_account, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/rooms/", self.get_user_rooms, methods=["GET"], response_model=RoomResponse)


    async def registration(self, data: RegUser, request: Request):
        if check_reg_data_correct(self.session, data):
            if verify_email(data.email):
                hashed_password = get_password_hash(data.password)
                self.session.add(User(data.username, data.email, hashed_password, online=False, regAt=datetime.utcnow(), locale=data.locale, ip=request.client.host))
                self.session.commit()
                return {"detail": "Successefuly registered new account", 'reg_data': data}

    async def log_in_for_access_token(self, data: LogInUser, request: Request):
        user = authenticate_user(self.session, str(data.username), str(data.password))
        if user.jwt is None:
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
        return {"detail": "Connection OK", "status": 200}
    
    # online requests
    async def delete_account(self, data: Token):
        self.session.query(User).filter(User.jwt == data.access_token).delete()
        self.session.commit()
        return {"detail": "Account successefuly deleted", "status": 200}
    
    async def get_user_rooms(self, token: str = Header(title="Authorization")):
        print(token)
        user = get_user_by_jwt(self.session, token)
        user_room_indexes = self.session.query(User__Room.roomId).filter(User__Room.memberId == user.id)
        user_rooms = self.session.query(Room).filter(Room.id == user_room_indexes)
        return {"user_rooms": []}
