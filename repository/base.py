from sqlalchemy.orm.session import sessionmaker

from db.base import Engine


class BaseRepository:
    
    def __init__(self):
        self.session = sessionmaker(bind=Engine)()
