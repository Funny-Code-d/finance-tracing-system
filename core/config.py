from email.policy import default
from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_CONNECT", cast=str, default='')

print(DATABASE_URL)