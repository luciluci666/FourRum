from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time

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
    hashed_password = Column("hashed_password", String(256), nullable=False)
    online = Column("online", Boolean, nullable=False)
    reg_date = Column("reg_date", Date)  
    locale = Column("locale", String(4))
    ip = Column("ip", String(16))
    last_active_datetime = Column("last_active_datetime", DateTime)
    jwt = Column("jwt", String(256))

    def __init__(self, username, email, hashed_password, online, reg_date=None, last_active_datetime=None, jwt=None, locale='en', ip=None):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.online = online
        self.reg_date = reg_date
        self.locale = locale   
        self.ip = ip
        self.last_active_datetime = last_active_datetime
        self.jwt = jwt

    def __repr__(self):
        return f"""{self.id}. username = {self.username} 
            email = {self.email} 
            hashed_password = {self.hashed_password} 
            online = {self.online} 
            regDate = {self.reg_date} 
            locale = {self.locale}
            ip = {self.ip}
            last_active_datetime = {self.last_active_datetime} 
            jwt = {self.jwt} """

if __name__ == "__main__":
    Database().create_tables()
