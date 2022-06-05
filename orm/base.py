from databases import Database
from db.base import database

class BaseEntity():
    
    def __init__(self):
        self.database = database