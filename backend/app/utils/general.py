from sqlalchemy.orm import sessionmaker
from datetime import datetime
from json import dumps

def get_session(engine):
    Session = sessionmaker(engine)
    session = Session()
    return session

def object_to_json(object):
    dict = object.__dict__
    del dict['_sa_instance_state']
    return dict

def delete_object(session, object):
    object.isDeleted = True
    object.deletedAt = datetime.utcnow()
    session.commit()
