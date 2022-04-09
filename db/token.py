import datetime
from sqlalchemy.schema import Sequence
from sqlalchemy import CheckConstraint, ForeignKey
import sqlalchemy
from .base import metadata


token_table = sqlalchemy.Table(
    "config_api",
    metadata,
    sqlalchemy.Column("token_id", sqlalchemy.Integer, Sequence("token_id_seq"),
                      server_default=Sequence("token_id_seq").next_value(), unique=True, nullable=False),
    sqlalchemy.Column("access_token", sqlalchemy.Text, primary_key=True),
    sqlalchemy.Column("refresh_token", sqlalchemy.Text, primary_key=True),
    sqlalchemy.Column("owner", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("email_owner", sqlalchemy.String(30), nullable=False),
    sqlalchemy.Column("date_create", sqlalchemy.DateTime, nullable=False, default=datetime.datetime.utcnow),
    sqlalchemy.Column("date_refresh", sqlalchemy.DateTime, nullable=False, default=datetime.datetime.utcnow),
)