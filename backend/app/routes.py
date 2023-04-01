from fastapi import APIRouter

from app.endpoints.internal_requests import InternalRequests
from app.endpoints.auth_requests import AuthRequests
from app.endpoints.account_requests import AccountRequests
from app.endpoints.room_requests import RoomRequests

from app.schemas import UserResponse, RoomResponse, User__RoomResponse
from app.schemas import UsersResponse, RoomsResponse, User__RoomsResponse
from app.schemas import Token, BasicResponse, RegResponse

class Routes:

    def __init__(self, engine, debug):
        self.router = APIRouter()
        self.engine = engine
        self.debug = debug

        # internal routes
        internal_request = InternalRequests(engine)

        self.router.add_api_route("/internal/users", internal_request.get_all_users, methods=["GET"], response_model=UsersResponse)
        self.router.add_api_route("/internal/rooms", internal_request.get_all_rooms, methods=["GET"], response_model=RoomsResponse)
        self.router.add_api_route("/internal/users__rooms", internal_request.get_all_user_room_realtionships, methods=["GET"], response_model=User__RoomsResponse)
        self.router.add_api_route("/internal/", internal_request.check_connection, methods=["GET"], response_model=BasicResponse)

        # authorization routes
        auth_request = AuthRequests(engine, debug)

        self.router.add_api_route("/reg", auth_request.registration, methods=["POST"], response_model=RegResponse)
        self.router.add_api_route("/login", auth_request.log_in_for_access_token, methods=["POST"], response_model=Token)

        # online routes (are working only with access token after logging in)

        # account routes
        account_request = AccountRequests(engine, debug)

        self.router.add_api_route("/user/delete", account_request.user_delete_account, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/account", account_request.user_get_my_account_info, methods=["GET"], response_model=UserResponse)

        # room routes
        room_request = RoomRequests(engine, debug)

        self.router.add_api_route("/user/room/", room_request.user_get_room_info, methods=["GET"], response_model=RoomResponse)
        self.router.add_api_route("/user/rooms/", room_request.user_get_rooms, methods=["GET"], response_model=RoomsResponse)

        self.router.add_api_route("/user/room/create", room_request.user_create_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/edit", room_request.user_edit_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/close", room_request.user_close_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/delete", room_request.user_delete_room, methods=["POST"], response_model=BasicResponse)
        self.router.add_api_route("/user/room/enter", room_request.user_enter_room, methods=["POST"], response_model=RoomResponse)
        self.router.add_api_route("/user/room/leave", room_request.user_leave_room, methods=["POST"], response_model=BasicResponse)