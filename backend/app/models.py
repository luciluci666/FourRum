from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
from config import MAIN_DB_URL

engine = create_engine(MAIN_DB_URL, echo=True)
meta = MetaData()


Users = Table(
    "Users",
    meta,
    Column("id", Integer, primary_key=True),
    Column("username", String(16), nullable=False),
    Column("email", String(64), nullable=False),
    Column("hashed_password", String(256), nullable=False),
    Column("online", Boolean, nullable=False),
    Column("reg_time", DateTime),  # print(datetime.utcnow()) # 2023-02-25 11:50:38.632948
    Column("last_log_in_time", DateTime),
)

if __name__ == "__main__":
    meta.create_all(engine)
