from datetime import datetime
from fastapi import Request

from app.database import User
from app.schemas import RegForm, LogInForm
from app.utils.general import get_session
from app.utils.auth_helpers import authenticate_user, create_access_token, get_password_hash, check_reg_data_correct, verify_email

class AuthRequests:
    
    def __init__(self, engine, debug):
        self.engine = engine
        self.debug = debug
        
    async def registration(self, data: RegForm, request: Request):
        if self.debug:
            print(data)
        session = get_session(self.engine)

        check_reg_data_correct(session, data)
        verify_email(data.email)
        hashed_password = get_password_hash(data.password)
        session.add(User(data.username, data.email, hashed_password, online=False, regAt=datetime.utcnow(), locale=data.locale, ip=request.client.host))
        session.commit()

        session.close()
        return {"detail": "Successefuly registered new account", 'reg_data': data}

    async def log_in_for_access_token(self, data: LogInForm, request: Request):
        if self.debug:
            print(data)
        session = get_session(self.engine)

        user = authenticate_user(session, str(data.username), str(data.password))
        access_token = create_access_token(user)
        user.jwt = access_token
        user.lastActiveAt = datetime.utcnow()
        user.ip = request.client.host
        session.commit()
        
        session.close()
        return {"access_token": access_token, "token_type": "bearer"}