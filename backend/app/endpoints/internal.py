from app.database import User, Room, User__Room
from app.utils.exceptions import SuccessefulResponse
from app.utils.general import get_session, object_to_json

class InternalRequests:

    def __init__(self, engine):
        self.engine = engine
        
    async def get_all_users(self):
        session = get_session(self.engine)
        json = get_all_json_of_objects_of_class(session, User, key_name="users")
        session.close()
        return json

    async def get_all_rooms(self):
        session = get_session(self.engine)
        json = get_all_json_of_objects_of_class(session, Room, key_name="rooms")
        session.close()
        return json
    
    async def get_all_user_room_realtionships(self):
        session = get_session(self.engine)
        json = get_all_json_of_objects_of_class(session, User__Room, key_name="user_room_relationships")
        session.close()
        return json
    
    async def check_connection(self):
        return SuccessefulResponse("Connection OK").json
    
def get_all_json_of_objects_of_class(session, data_class, key_name, add_deleted=False):
    my_json = {
        key_name: []
    }
    objects = session.query(data_class).all()
    for object in objects:
        if add_deleted and not object.isDeleted:
            object = object_to_json(object)
            my_json[key_name].append(object)
    return my_json
    