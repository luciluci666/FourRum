from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy import create_engine

BASE = declarative_base()


class Database:
    def __init__(self, db_url, config):
        self.engine = create_engine(db_url, 
            pool_size=config['pool_size'],
            pool_timeout=config['pool_timeout'],
            pool_recycle=config['pool_recycle'],
            max_overflow=config['max_overflow'],
            echo=config['echo'])
        try: 
            BASE.metadata.create_all(self.engine)
        except Exception:
            print("There alredy are tables in database")


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

class Room(BASE):
    __tablename__ = "Rooms"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(32), nullable=False)
    description = Column("description", String(128), nullable=False)
    type = Column("type", String(16), nullable=False)
    colour = Column("colour", String(8), nullable=False)
    creatorId = Column("creatorId", Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    isPrivate = Column("isPrivate", Boolean, nullable=False)
    createdAt = Column("createdAt", DateTime, nullable=False)
    isClosed = Column("isClosed", Boolean, nullable=True)
    isDeleted = Column("isDeleted", Boolean, nullable=False)
    deletedAt = Column("deletedAt", DateTime)

    def __init__(self, title, description, type, colour, creatorId, createdAt, isPrivate=False, isClosed=False, isDeleted=False, deletedAt=None):
        self.title = title
        self.description = description
        self.type = type # group, channel, thread, discussion
        self.colour = colour # hex rgb
        self.creatorId = creatorId
        self.createdAt = createdAt
        self.isPrivate = isPrivate
        self.isClosed = isClosed # for threads and duscussions
        self.isDeleted = isDeleted
        self.deletedAt = deletedAt

    def __repr__(self):
        return f"""{self.id}. title: {self.title} 
            description: {self.description}
            type: {self.type}
            isPrivate: {self.isPrivate}
            colour: {self.colour} 
            creatorId: {self.creatorId} 
            createdAt: {self.createdAt}
            isClosed: {self.isClosed}
            isDeleted: {self.isDeleted}
            deletedAt: {self.deletedAt} """

class User__Room(BASE):
    __tablename__ = "Users__Rooms"

    id = Column("id", Integer, primary_key=True)
    userId = Column("userId", Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    roomId = Column("roomId", Integer, ForeignKey("Rooms.id", ondelete="CASCADE"), nullable=False)
    userJoinedAt = Column("userJoinedAt", DateTime, nullable=False)
    hasAdminRights = Column("hasAdminRights", Boolean, nullable=False)
    userWasKicked = Column("userWasKicked", Boolean, nullable=False)
    isDeleted = Column("isDeleted", Boolean, nullable=False)
    deletedAt = Column("deletedAt", DateTime)

    def __init__(self, userId, roomId, userJoinedAt, hasAdminRights=False, userWasKicked=False, isDeleted=False, deletedAt=None):
        self.userId = userId
        self.roomId = roomId
        self.userJoinedAt = userJoinedAt
        self.hasAdminRights = hasAdminRights 
        self.userWasKicked = userWasKicked
        self.isDeleted = isDeleted
        self.deletedAt = deletedAt

    def __repr__(self):
        return f"""{self.id}.  
            userId: {self.userId}  
            roomId: {self.roomId}
            userJoinedAt: {self.userJoinedAt}
            hasAdminRights: {self.hasAdminRights}
            userWasKicked: {self.userWasKicked}
            isDeleted: {self.isDeleted}
            deletedAt: {self.deletedAt} """
