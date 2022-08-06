# from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from core.config import DATABASE_URL


# database = Database(DATABASE_URL)
# metadata = MetaData()
Engine = create_engine(DATABASE_URL)
DecBase = declarative_base()
