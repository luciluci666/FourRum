class Room:
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
