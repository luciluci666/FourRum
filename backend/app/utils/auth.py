import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from re import fullmatch

from config import JWT_KEY, JWT_ENCODING, JWT_EXPIRE_MINUTES
from app.schemas import RegForm
from app.database import User
from app.utils.exceptions import AuthException, ValidationException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
email_scheme = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def get_user_by_username(session, username: str):
    user = session.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The account you are trying to access can not be found"
        )
    elif user.isDeleted:
        raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="The account you are trying to access was deleted"
        )
    else:
        return user
        
# registration
def check_reg_data_correct(session, data: RegForm):
    if (not data.username) or (not data.email) or (not data.password):
        raise ValidationException("Username, email, and password can't be empty").exception
    else:
        duplicate_username = session.query(User).filter(User.username == data.username).first()
        duplicate_email = session.query(User).filter(User.email == data.email).first()
        if duplicate_username:
            if not duplicate_username.isDeleted:
                raise ValidationException("There already is an account with such username").exception
        elif duplicate_email:
            if not duplicate_email.isDeleted:
                raise ValidationException("There already is an account with such email").exception
        elif not fullmatch(email_scheme, data.email):
            raise ValidationException("Email spelling is incorrect").exception
        elif len(data.password) < 8:
            raise ValidationException("Password is too small, it should have at least 8 symbols").exception
        elif len(data.locale) > 2:
            raise ValidationException("Incorrect locale parameter").exception
        return data

def verify_email(email):
    return True
            
def get_password_hash(password):
    return pwd_context.hash(password)


# authorization
def authenticate_user(session, username: str, password: str):
    user = get_user_by_username(session, username)
    if not pwd_context.verify(password, user.hashedPassword):
        raise AuthException("Incorrect username or password").exception
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
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=JWT_ENCODING)
        jwt_username = payload.get("username")
    except jwt.ExpiredSignatureError:
        raise AuthException("Access token expired").exception
    except (jwt.InvalidTokenError, jwt.InvalidSignatureError):
        raise AuthException("Invalid access token").exception
    except:
        raise AuthException("Cpuld not validate credentials").exception
    user = get_user_by_username(session, username=jwt_username)
    user.lastActiveAt = datetime.utcnow()
    session.commit()
    return user
