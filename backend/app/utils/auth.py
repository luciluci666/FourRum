from jose import JWTError, jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from re import fullmatch

from config import JWT_KEY, JWT_ENCODING, JWT_EXPIRE_MINUTES
from app.schemas import RegUser
from app.database import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
email_scheme = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

class AuthException(Exception):

    def __init__(self):
        self.exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Registration or Authorization Error"
        )

        
# registration
def check_reg_data_correct(session, data: RegUser):
    exception = AuthException().exception
    if (not data.username) or (not data.email) or (not data.password):
        exception.detail = "Username, email, and password can't be empty"
        raise exception
    else:
        duplicate_username = get_user(session, data.username)
        duplicate_email = session.query(User).filter(User.email == data.email).first()
        if duplicate_username:
            exception.detail = "There alredy is an account with such username"
            raise exception
        elif duplicate_email:
            exception.detail = "There alredy is an account with such email"
            raise exception
        elif not fullmatch(email_scheme, data.email):
            exception.detail = "Email spelling is incorrect"
            raise exception
        elif len(data.password) < 8:
            exception.detail = "Password is too small, it should have at least 8 symbols"
            raise exception
        else:
            return data

def verify_email(email):
    return True
            
def get_password_hash(password):
    return pwd_context.hash(password)


# authorization
def get_user(session, username: str):
    user = session.query(User).filter(User.username == username).first()
    if user:
        return user

def authenticate_user(session, username: str, password: str):
    exception = AuthException().exception
    exception.detail="Incorrect username or password"

    user = get_user(session, username)
    if not user:
        raise exception
    if not pwd_context.verify(password, user.hashed_password):
        raise exception
    return user

def create_access_token(user: User):
    payload = {
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES),
        'iat': datetime.utcnow(),
        'iss': 'FourRoom',
    }
    encoded_jwt = jwt.encode(payload, JWT_KEY, algorithm=JWT_ENCODING)
    return encoded_jwt

def get_user_by_jwt(session, token: str):
    exception = AuthException().exception
    exception.detail="Could not validate credentials"
    try:
        payload = jwt.decode(token, JWT_KEY, algorithm=JWT_ENCODING)
        if payload.get("exp") < datetime.utcnow():
            exception.detail="JWT expired"
            raise exception
        else:
            jwt_username = payload.get("username")
    except JWTError:
        raise exception
    user = get_user(session, username=jwt_username)
    if user is None:
        raise exception
    return user
