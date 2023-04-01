from fastapi import APIRouter, Request, Depends, Header

router = APIRouter()

router.add_api_route("/users", get_all_users, methods=["GET"], response_model=UsersResponse)
router.add_api_route("/rooms", get_all_rooms, methods=["GET"], response_model=RoomsResponse)
router.add_api_route("/user__rooms", get_all_user_room_realtionships, methods=["GET"], response_model=User__RoomsResponse)
router.add_api_route("/", check_connection, methods=["GET"], response_model=BasicResponse)

# authorization routes
router.add_api_route("/reg", registration, methods=["POST"], response_model=RegResponse)
router.add_api_route("/login", log_in_for_access_token, methods=["POST"], response_model=Token)

# online routes (are working only with access token after logging in)

# account routes
router.add_api_route("/user/delete", user_delete_account, methods=["POST"], response_model=BasicResponse)
router.add_api_route("/user/account", user_get_my_account_info, methods=["GET"], response_model=UserResponse)

# room routes
router.add_api_route("/user/room/", user_get_room_info, methods=["GET"], response_model=RoomResponse)
router.add_api_route("/user/rooms/", user_get_rooms, methods=["GET"], response_model=RoomsResponse)

router.add_api_route("/user/room/create", user_create_room, methods=["POST"], response_model=BasicResponse)
router.add_api_route("/user/room/edit", user_edit_room, methods=["POST"], response_model=BasicResponse)
router.add_api_route("/user/room/close", user_close_room, methods=["POST"], response_model=BasicResponse)
router.add_api_route("/user/room/delete", user_delete_room, methods=["POST"], response_model=BasicResponse)
router.add_api_route("/user/room/enter", user_enter_room, methods=["POST"], response_model=RoomResponse)
router.add_api_route("/user/room/leave", user_leave_room, methods=["POST"], response_model=BasicResponse)