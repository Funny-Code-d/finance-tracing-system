from sqlalchemy.schema import Sequence
from sqlalchemy import CheckConstraint, ForeignKey
import sqlalchemy
from .base import metadata


customers = sqlalchemy.Table(
    "customers",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("token_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("config_api.token_id"), nullable=False),
    sqlalchemy.Column("first_name", sqlalchemy.String(20)),
    sqlalchemy.Column("last_name", sqlalchemy.String(20)),
    sqlalchemy.Column("email", sqlalchemy.String(100), unique=True),
    sqlalchemy.Column("telegram_id", sqlalchemy.Integer, unique=True)
)