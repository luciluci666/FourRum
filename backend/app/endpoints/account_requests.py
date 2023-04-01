from fastapi import Header

from app.utils.exceptions import SuccessefulResponse

from app.utils.general import get_session, object_to_json, delete_object
from app.utils.auth_helpers import get_user_by_jwt

class AccountRequests:

    def __init__(self, engine, debug):
        self.engine = engine
        self.debug = debug
        

    async def user_delete_account(self, token: str = Header(title="Authorization")):
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)

        delete_object(session, user)
        session.commit()

        session.close()
        return SuccessefulResponse("Account successefuly deleted").json
    
    async def user_get_my_account_info(self, token: str = Header(title="Authorization")):
        session = get_session(self.engine)
        user = get_user_by_jwt(session, token)

        user = object_to_json(user)
        
        session.close()
        return {"user": user}