from databases import Database


class BaseRepository():
    
    def __init__(self, db_orm: Database):
        self.db_orm = db_orm