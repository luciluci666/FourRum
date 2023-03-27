from sqlalchemy.orm import sessionmaker
from datetime import datetime

def get_session(engine):
    Session = sessionmaker(engine)
    session = Session()
    return session

def object_to_json(object):
    dict = object.__dict__
    del dict['_sa_instance_state']
    return dict

def get_all_json_of_objects_of_class(session, data_class, key_name, add_deleted=False):
    my_json = {
        key_name: []
    }
    objects = session.query(data_class).all()
    for object in objects:
        if (not add_deleted) and object.isDeleted:
            pass
        else:
            object = object_to_json(object)
            my_json[key_name].append(object)
    return my_json

def delete_object(session, object):
    object.isDeleted = True
    object.deletedAt = datetime.utcnow()
    session.commit()