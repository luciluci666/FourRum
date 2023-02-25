import os

MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MAIN_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")


JWT_KEY = os.getenv("JWT_KEY")