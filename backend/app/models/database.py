from sqlalchemy.ext.declarative import declarative_base
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