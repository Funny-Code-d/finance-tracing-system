from email.policy import default
from starlette.config import Config

config = Config(".env")

# DATABASE_URL = config("DATABASE_CONNECT", cast=str, default='')
DATABASE_URL = "postgresql://postgres:tinkerTHEbest***10122001@finance-tracking.ru:32700/api_system"