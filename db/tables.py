from enum import unique
# from typing import Sequence
from sqlalchemy.schema import Sequence

import sqlalchemy
from .base import metadata


token = sqlalchemy.Table(
    "config_api",
    metadata,
    sqlalchemy.Column("token_id", sqlalchemy.Integer, Sequence("token_id_seq"),
                      server_default=Sequence("token_id_seq").next_value(), unique=True),
    sqlalchemy.Column("token", sqlalchemy.String(30), primary_key=True),
    sqlalchemy.Column("owner", sqlalchemy.String(50)),
    sqlalchemy.Column("application", sqlalchemy.String(10)),
)

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

category = sqlalchemy.Table(
    "category",
    metadata,
    sqlalchemy.Column("category_id", sqlalchemy.Integer, Sequence("category_id_seq"),
                      server_default=Sequence("category_id_seq").next_value(), unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("customers.user_id"), nullable=False),
    sqlalchemy.Column("name_category", sqlalchemy.String(30), nullable=False),
    sqlalchemy.PrimaryKeyConstraint("user_id", "name_category", name='category_pk')
)

personal_view = sqlalchemy.Table(
    "personal_view",
    metadata,
    sqlalchemy.Column("view_id", sqlalchemy.Integer, Sequence("view_id_seq"),
                      server_default=Sequence("view_id_seq").next_value(), unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("customers.user_id"), nullable=False),
    sqlalchemy.Column("name_view", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("number_days", sqlalchemy.Integer, nullable=False),
    sqlalchemy.PrimaryKeyConstraint("user_id", "name_view", name="personal_view_pk")
)

settings_view = sqlalchemy.Table(
    "settings_view",
    metadata,
    sqlalchemy.Column("view_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("personal_view.view_id"), nullable=False),
    sqlalchemy.Column("category_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("category.category_id"), nullable=False),
    sqlalchemy.PrimaryKeyConstraint("view_id", "category_id", name="settings_view_pk")
)


purchase = sqlalchemy.Table(
    "purchase",
    metadata,
    sqlalchemy.Column("purchase_id", sqlalchemy.Integer, unique=True, autoincrement=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("customers.user_id"), nullable=False),
    sqlalchemy.Column("total_amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("category", sqlalchemy.Integer, sqlalchemy.ForeignKey("category.category_id"), nullable=False),
    sqlalchemy.Column("date_purchase", sqlalchemy.Date, nullable=False),
    sqlalchemy.PrimaryKeyConstraint("purchase_id", "user_id", name="purchase_pk")
)

details_purchase = sqlalchemy.Table(
    "details_purchase",
    metadata,
    sqlalchemy.Column("details_purchase_id", sqlalchemy.Integer, autoincrement=True, primary_key=True),
    sqlalchemy.Column("purchase_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("purchase.purchase_id")),
    sqlalchemy.Column("name_product", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("quantity", sqlalchemy.Integer),
)


