import datetime
from sqlalchemy.schema import Sequence
from sqlalchemy import CheckConstraint, ForeignKey, Column
from sqlalchemy import String, Integer, Text, Boolean, Float, DateTime
import sqlalchemy
from .base import metadata


link_token_customer = sqlalchemy.Table(
    "link_token_customer",
    metadata,
    Column("token_sk", Integer, ForeignKey("hub_token.token_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("customer_sk", Integer, ForeignKey("hub_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


link_customer_debtor = sqlalchemy.Table(
    "link_customer_debtor",
    metadata,
    Column("customer_sk", Integer, ForeignKey("hub_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("debtor_sk", String(100), ForeignKey("hub_debtor.debtor_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


link_debtor_debtbook = sqlalchemy.Table(
    "link_debtor_debtbook",
    metadata,
    Column("debtor_sk", String(100), ForeignKey("hub_debtor.debtor_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("debtbook_sk", Integer, ForeignKey("hub_debtbook.debtbook_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


link_admin_group = sqlalchemy.Table(
    "link_admin_group",
    metadata,
    Column("customer_sk", Integer, ForeignKey("hub_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("group_sk", String(100), ForeignKey("hub_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


link_pull_group = sqlalchemy.Table(
    "link_pull_group",
    metadata,
    Column("customer_sk", Integer, ForeignKey("hub_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("group_sk", String(100), ForeignKey("hub_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


link_group_todo_list = sqlalchemy.Table(
    "link_group_todo_list",
    metadata,
    Column("group_sk", String(100), ForeignKey("hub_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("todo_list_sk", Integer, ForeignKey("hub_todo_list.todo_list_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


link_templates_group = sqlalchemy.Table(
    "link_templates_group",
    metadata,
    Column("template_sk", Integer, ForeignKey("hub_templates.template_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("group_sk", String(100), ForeignKey("hub_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


link_group_category = sqlalchemy.Table(
    "link_group_category",
    metadata,
    Column("group_sk", String(100), ForeignKey("hub_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("category_sk", Integer, ForeignKey("hub_category.category_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


link_templates_category = sqlalchemy.Table(
    "link_templates_category",
    metadata,
    Column("template_sk", Integer, ForeignKey("hub_templates.template_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("category_sk", Integer, ForeignKey("hub_category.category_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


link_purchase_category = sqlalchemy.Table(
    "link_purchase_category",
    metadata,
    Column("purcahse_sk", Integer, ForeignKey("hub_purchase.purchase_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("category_sk", Integer, ForeignKey("hub_category.category_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


link_purcahse_group = sqlalchemy.Table(
    "link_purchase_group",
    metadata,
    Column("purchase_sk", Integer, ForeignKey("hub_purchase.purchase_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("group_sk", String(100), ForeignKey("hub_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)