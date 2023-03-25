from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from time import sleep

from config import MAIN_DB_URL
from app.handlers import Handlers
from app.database import Database


sleep(2)
DEBUG = True
ENGINE = create_engine(MAIN_DB_URL, echo=DEBUG)

try:
    Database(ENGINE).create_tables()
except Exception as e:
    print(e)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=Handlers(ENGINE, DEBUG).router)

# if __name__ == "__main__":
#     main()
