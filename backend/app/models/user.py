from sqlalchemy import Column, Integer, String, Boolean, DateTime

from .database import BASE


class User(BASE):
    __tablename__ = "Users"

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String(16), nullable=False)
    email = Column("email", String(64), nullable=False)
    hashedPassword = Column("hashedPassword", String(256), nullable=False)
    online = Column("online", Boolean, nullable=False)
    regAt = Column("regAt", DateTime, nullable=False)
    ip = Column("ip", String(16), nullable=False)
    locale = Column("locale", String(4), nullable=False)
    lastActiveAt = Column("lastActiveAt", DateTime)
    jwt = Column("jwt", String(256))
    isDeleted = Column("isDeleted", Boolean, nullable=False)
    deletedAt = Column("deletedAt", DateTime)

    def __init__(self, username, email, hashedPassword, online, regAt, ip, locale='en', lastActiveAt=None, jwt=None, isDeleted=False, deletedAt=None):
        self.username = username
        self.email = email
        self.hashedPassword = hashedPassword
        self.online = online
        self.regAt = regAt
        self.ip = ip
        self.locale = locale   
        self.lastActiveAt = lastActiveAt
        self.jwt = jwt
        self.isDeleted = isDeleted
        self.deletedAt = deletedAt

    def __repr__(self):
        return f"""{self.id}. username: {self.username} 
            email: {self.email} 
            hashedPassword: {self.hashedPassword} 
            online: {self.online} 
            regAt: {self.regAt} 
            locale: {self.locale}
            ip: {self.ip}
            lastActiveAt: {self.lastActiveAt} 
            jwt: {self.jwt}
            isDeleted: {self.isDeleted}
            deletedAt: {self.deletedAt} """

