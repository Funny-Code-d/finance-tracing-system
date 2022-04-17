import datetime
from sqlalchemy.schema import Sequence
from sqlalchemy import CheckConstraint, ForeignKey, Column
from sqlalchemy import String, Integer, Text, Boolean, Float
import sqlalchemy
from .base import metadata


hub_token = sqlalchemy.Table(
    "hub_token",
    metadata,
    Column("token_sk", Integer, primary_key=True, autoincrement=True),
    Column("access_token", Text, unique=True, nullable=False),
    Column("refresh_token", Text, unique=True, nullable=False)
)

hub_customer = sqlalchemy.Table(
    "hub_customer",
    metadata,
    Column("customer_sk", Integer, primary_key=True, autoincrement=True),
    Column("email", String(30), unique=True, nullable=True),
    Column("telegram_id", Integer, unique=True, nullable=True),
    Column("password", Text, unique=True, nullable=True)
)

hub_group = sqlalchemy.Table(
    "hub_group",
    metadata,
    #Column("group_sk", Integer, primary_key=True, autoincrement=True),
    Column("group_sk", String(100), primary_key=True),
    Column("access", String(10), nullable=False),
)

hub_todo_list = sqlalchemy.Table(
    "hub_todo_list",
    metadata,
    Column("todo_list_sk", Integer, primary_key=True, autoincrement=True),
    Column("name_todo_list", String(50), nullable=False),
    Column("is_active", Boolean, nullable=False)
)

hub_category = sqlalchemy.Table(
    "hub_category",
    metadata,
    Column("category_sk", Integer, primary_key=True, autoincrement=True),
    Column("name_category", String(30), nullable=False)
)

hub_templates = sqlalchemy.Table(
    "hub_templates",
    metadata,
    Column("template_sk", Integer, primary_key=True, autoincrement=True),
    Column("name_template", String(30), nullable=False),
    Column("number_days", Integer, nullable=False)
)

hub_purchase = sqlalchemy.Table(
    "hub_purchase",
    metadata,
    Column("purchase_sk", Integer, primary_key=True, autoincrement=True),
    Column("name_store", String(50), nullable=True)
)

hub_debtor = sqlalchemy.Table(
    "hub_debtor",
    metadata,
    Column("debtor_sk", String(100), primary_key=True)
)

hun_debtbook = sqlalchemy.Table(
    "hub_debtbook",
    metadata,
    Column("debtbook_sk", Integer, primary_key=True, autoincrement=True),
    Column("type_action", String(10), nullable=False),
    Column("total_amount", Float, nullable=False)
)
