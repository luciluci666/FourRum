from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from time import sleep

from config import MAIN_DB_URL
from app.urls import router
from app.database import Database

sleep(2)

DEBUG = True
DB_CONFIG = {
    'pool_size': 10,
    'pool_timeout': 30,
    'pool_recycle': 3600,
    'max_overflow': 10,
    'echo': DEBUG,
}

ENGINE = Database(MAIN_DB_URL, DB_CONFIG).engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=router)

# if __name__ == "__main__":
#     main()
