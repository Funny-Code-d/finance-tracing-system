# from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from core.config import Config


# database = Database(DATABASE_URL)
# metadata = MetaData()
Engine = create_engine(Config.DATABASE_CONNECT_URI)
DecBase = declarative_base()
