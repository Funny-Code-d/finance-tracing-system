import datetime
from sqlalchemy.schema import Sequence
from sqlalchemy import CheckConstraint, ForeignKey, Column
from sqlalchemy import String, Integer, Text, Boolean, Float, DateTime
import sqlalchemy
from .base import metadata


sat_token = sqlalchemy.Table(
    "sat_token",
    metadata,
    Column("token_sk", Integer, ForeignKey("hub_token.token_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("name_owner", String(50), nullable=False),
    Column("email_owner", String(50), nullable=False),
    Column("date_create", DateTime, nullable=False, default=datetime.datetime.utcnow)
)


sat_customer = sqlalchemy.Table(
    "sat_customer",
    metadata,
    Column("customer_sk", Integer, ForeignKey("hub_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("first_name", String(30), nullable=True),
    Column("last_name", String(30), nullable=True)
)

sat_group = sqlalchemy.Table(
    "sat_group",
    metadata,
    Column("group_sk", String(100), ForeignKey("hub_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("name_group", String(50), nullable=False),
    Column("description", Text, nullable=True)
)

sat_debtor = sqlalchemy.Table(
    "sat_debtor",
    metadata,
    Column("debtor_sk", Integer, ForeignKey("hub_debtor.debtor_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("first_name", String(30), nullable=True),
    Column("last_name", String(30), nullable=True),
    Column("telegram_id", Integer, nullable=True)
)

sat_debtbook_history = sqlalchemy.Table(
    "sat_debtbook_history",
    metadata,
    Column("debtbook_history_sk", Integer, primary_key=True, autoincrement=True),
    Column("debtbook_sk", Integer, ForeignKey("hub_debtbook.debtbook_sk", ondelete="CASCADE", onupdate="CASCADE")),
    Column("action", String(10), nullable=False),
    Column("amount", Float, nullable=False),
    Column("date_regist", DateTime, nullable=False, default=datetime.datetime.utcnow)
)


sat_item_todo_list = sqlalchemy.Table(
    "sat_item_todo_list",
    metadata,
    Column("todo_list_sk", Integer, ForeignKey("hub_todo_list.todo_list_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("item_todo_list_sk", Integer, primary_key=True, autoincrement=True),
    Column("name_item", String(30), nullable=False),
    Column("price", Float, nullable=True),
    Column("quantity", Integer, nullable=True),
    Column("complited", Boolean, nullable=False),
)


sat_purchase = sqlalchemy.Table(
    "sat_purchase",
    metadata,
    Column("purchase_sk", Integer, ForeignKey("hub_purchase.purchase_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("total_amount", Float, nullable=False)
)

sat_purchase_detail = sqlalchemy.Table(
    "sat_purchase_detail",
    metadata,
    Column("purchase_detail_sk", Integer, primary_key=True, autoincrement=True),
    Column("purchase_sk", Integer, ForeignKey("hub_purchase.purchase_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("name_product", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("quantity", Integer, nullable=True)
)

sat_friends = sqlalchemy.Table(
    "sat_friends",
    metadata,
    Column("customer1_sk", Integer, ForeignKey("hub_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("customer2_sk", Integer, ForeignKey("hub_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("status", Integer, nullable=False)
)
