from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import MAIN_DB_URL
from app.routes import Routes
from app.models import Database


DEBUG = True
DB_CONFIG = {
    'pool_size': 10,
    'pool_timeout': 30,
    'pool_recycle': 3600,
    'max_overflow': 10,
    'echo': False,
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
app.include_router(router=Routes(ENGINE, DEBUG).router)

# if __name__ == "__main__":
#     main()
