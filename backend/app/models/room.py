from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from .database import BASE


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
