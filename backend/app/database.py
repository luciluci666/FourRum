from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, ForeignKey

BASE = declarative_base()


class Database:

    def __init__(self, engine):
        self.engine = engine

    def create_tables(self):
        BASE.metadata.create_all(self.engine)


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

    def __init__(self, username, email, hashedPassword, online, regAt, ip, locale='en', lastActiveAt=None, jwt=None):
        self.username = username
        self.email = email
        self.hashedPassword = hashedPassword
        self.online = online
        self.regAt = regAt
        self.ip = ip
        self.locale = locale   
        self.lastActiveAt = lastActiveAt
        self.jwt = jwt

    def __repr__(self):
        return f"""{self.id}. username: {self.username} 
            email: {self.email} 
            hashedPassword: {self.hashedPassword} 
            online: {self.online} 
            regAt: {self.regAt} 
            locale: {self.locale}
            ip: {self.ip}
            lastActiveAt: {self.lastActiveAt} 
            jwt: {self.jwt} """

class Room(BASE):
    __tablename__ = "Rooms"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(16), nullable=False)
    description = Column("description", String(128), nullable=False)
    type = Column("type", String(16), nullable=False)
    colour = Column("colour", String(8), nullable=False)
    creatorId = Column("creatorId", Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    createdAt = Column("createdAt", DateTime, nullable=False)

    def __init__(self, title, description, colour, type, creatorId, createdAt):
        self.title = title
        self.description = description
        self.type = type # group, channel, thread, discussion 
        self.colour = colour
        self.creatorId = creatorId
        self.createdAt = createdAt   

    def __repr__(self):
        return f"""{self.id}. title: {self.title} 
            description: {self.description}
            type: {self.type}  
            colour: {self.colour} 
            creatorId: {self.creatorId} 
            createdAt: {self.createdAt} """

class User__Room(BASE):
    __tablename__ = "Users__Rooms"

    id = Column("id", Integer, primary_key=True)
    roomId = Column("roomId", Integer, ForeignKey("Rooms.id", ondelete="CASCADE"), nullable=False)
    memberId = Column("memberId", Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    memberAddedAt = Column("memberAddedAt", DateTime, nullable=False)

    def __init__(self, roomId, memberId, memberAddedAt):
        self.roomId = roomId
        self.memberId = memberId
        self.memberAddedAt = memberAddedAt 

    def __repr__(self):
        return f"""{self.id}.  
            roomId: {self.roomId}
            memberId: {self.memberId}  
            memberAddedAt: {self.memberAddedAt} """
