from enum import unique
from sqlalchemy.schema import Sequence
from sqlalchemy import CheckConstraint, ForeignKey
import sqlalchemy
from .base import metadata


token = sqlalchemy.Table(
    "config_api",
    metadata,
    sqlalchemy.Column("token_id", sqlalchemy.Integer, Sequence("token_id_seq"),
                      server_default=Sequence("token_id_seq").next_value(), unique=True, nullable=False),
    sqlalchemy.Column("access_token", sqlalchemy.String(30), primary_key=True),
    sqlalchemy.Column("refresh_token", sqlalchemy.String(30), primary_key=True),
    sqlalchemy.Column("owner", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("email_owner", sqlalchemy.String(30), nullable=False),
    sqlalchemy.Column("date_create", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("date_refresh", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("date_end", sqlalchemy.Date, nullable=False)
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

debt_person = sqlalchemy.Table(
    "debt_person",
    metadata,
    sqlalchemy.Column("debtor_id", sqlalchemy.Integer, Sequence("debt_id_seq"), server_default=Sequence("debt_id_seq").next_value(), unique=True, nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("customers.user_id"), nullable=False),
    sqlalchemy.Column("name_debtor", sqlalchemy.String(50), nullable=False),
    sqlalchemy.PrimaryKeyConstraint("user_id", "name_debtor")
)


debtbook = sqlalchemy.Table(
    "debtbook",
    metadata,
    sqlalchemy.Column("debtor_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("debt_person.debtor_id"), nullable=False),
    sqlalchemy.Column("type_action", sqlalchemy.String(4), CheckConstraint("type_action in ('take', 'give')"), nullable=False),
    sqlalchemy.Column("total_amount", sqlalchemy.Float, default=0, nullable=False),
    sqlalchemy.PrimaryKeyConstraint("debtor_id", "type_action", name="debtbook_pk")
)

debtbook_history = sqlalchemy.Table(
    "debtbook_history",
    metadata,
    sqlalchemy.Column("record_id", sqlalchemy.Integer, Sequence("record_id_seq"), server_default=Sequence("record_id_seq").next_value(), unique=True, nullable=False),
    sqlalchemy.Column("debtor_id", sqlalchemy.Integer, ForeignKey("debt_person.debtor_id"), nullable=False),
    sqlalchemy.Column("type_action", sqlalchemy.String(4), CheckConstraint("type_action in ('take', 'give')"), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("date_registration", sqlalchemy.Date, nullable=False),
    sqlalchemy.PrimaryKeyConstraint("record_id", name="debtbook_history_pk")
)

# personal tables

personal_group = sqlalchemy.Table(
    "personal_cost_group",
    metadata,
    sqlalchemy.Column("group_id", sqlalchemy.Integer, Sequence("personal_cost_group_seq"), server_default=Sequence("personal_cost_group_seq").next_value(), unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("name_group", sqlalchemy.Integer, ForeignKey("customers.user_id"), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=True),
    sqlalchemy.PrimaryKeyConstraint("user_id", "name_group", name="personal_cost_group_pk")
)

personal_category = sqlalchemy.Table(
    "personal_category",
    metadata,
    sqlalchemy.Column("category_id", sqlalchemy.Integer, Sequence("personal_category_seq"), server_default=Sequence("personal_category_seq").next_value(), unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("name_category", sqlalchemy.String(30)),
    sqlalchemy.PrimaryKeyConstraint("user_id", "name_category", name="personal_category_pk")
)

personal_purchase = sqlalchemy.Table(
    "personal_purchase",
    metadata,
    sqlalchemy.Column("purchase_id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("group_id", sqlalchemy.Integer, ForeignKey("personal_cost_group.group_id"), nullable=False),
    sqlalchemy.Column("total_amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("category_id", sqlalchemy.Integer, ForeignKey("personal_category.category_id")),
    sqlalchemy.Column("date_registration", sqlalchemy.Date, nullable=False)
)

detail_personal_purchase = sqlalchemy.Table(
    "detail_personal_purchase",
    metadata,
    sqlalchemy.Column("detail_purchase_id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("purchase_id", sqlalchemy.Integer, ForeignKey("personal_purchase.purchase_id"), nullable=False),
    sqlalchemy.Column("name_product", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("quantity", sqlalchemy.Integer, nullable=True)
)

personal_temlates = sqlalchemy.Table(
    "personal_templates",
    metadata,
    sqlalchemy.Column("template_id", sqlalchemy.Integer, Sequence("template_id_seq"), server_default=Sequence("template_id_seq").next_value(), unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey("customers.user_id"), nullable=False),
    sqlalchemy.Column("name_template", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("number_days", sqlalchemy.Integer, nullable=False),
    sqlalchemy.PrimaryKeyConstraint("user_id", "name_template", name="personal_templates_pk")
)

personal_templates_category = sqlalchemy.Table(
    "personal_templates_category",
    metadata,
    sqlalchemy.Column("template_id", sqlalchemy.Integer, ForeignKey("personal_templates.template_id"), primary_key=True),
    sqlalchemy.Column("category_id", sqlalchemy.Integer, ForeignKey("personal_category.category_id"), primary_key=True)
)

# public tables

public_group = sqlalchemy.Table(
    "public_cost_group",
    metadata,
    sqlalchemy.Column("group_id", sqlalchemy.Integer, Sequence("public_cost_group_seq"), server_default=Sequence("public_cost_group_seq").next_value(), unique=True, nullable=False),
    sqlalchemy.Column("admin_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("name_group", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=True),
    sqlalchemy.PrimaryKeyConstraint("admin_id", "name_group", name="public_cost_group_pk")
)

public_group_users = sqlalchemy.Table(
    "public_cost_group_users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey("customers.user_id"), primary_key=True),
    sqlalchemy.Column("group_id", sqlalchemy.Integer, ForeignKey("public_cost_group.group_id"), primary_key=True)
)

public_category = sqlalchemy.Table(
    "public_category",
    metadata,
    sqlalchemy.Column("category_id", sqlalchemy.Integer, Sequence("public_category_seq"), server_default=Sequence("public_category_seq").next_value(), unique=True),
    sqlalchemy.Column("group_id", sqlalchemy.Integer, ForeignKey("public_cost_group.group_id")),
    sqlalchemy.Column("name_category", sqlalchemy.String(30)),
    sqlalchemy.PrimaryKeyConstraint("group_id", "name_category", name="public_category_pk")
)

public_purchase = sqlalchemy.Table(
    "public_purchase",
    metadata,
    sqlalchemy.Column("purchase_id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("group_id", sqlalchemy.Integer, ForeignKey("public_cost_group.group_id"), nullable=False),
    sqlalchemy.Column("total_amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("category_id", sqlalchemy.Integer, ForeignKey("public_category.category_id"), nullable=False),
    sqlalchemy.Column("date_registration", sqlalchemy.Date, nullable=False)
)

detail_public_purchase = sqlalchemy.Table(
    "detail_public_purchase",
    metadata,
    sqlalchemy.Column("detail_purchase_id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("purchase_id", sqlalchemy.Integer, ForeignKey("public_purchase.purchase_id"), nullable=False),
    sqlalchemy.Column("name_product", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("quantity", sqlalchemy.Integer, nullable=True)
)

public_templates = sqlalchemy.Table(
    "public_templates",
    metadata,
    sqlalchemy.Column("template_id", sqlalchemy.Integer, Sequence("public_templates_seq"), server_default=Sequence("public_templates_seq").next_value(), unique=True),
    sqlalchemy.Column("group_id", sqlalchemy.Integer, ForeignKey("public_cost_group.group_id")),
    sqlalchemy.Column("name_template", sqlalchemy.String(30)),
    sqlalchemy.Column("number_days", sqlalchemy.Integer),
    sqlalchemy.PrimaryKeyConstraint("group_id", "name_template", name="public_templates_pk")
)

public_templates_category = sqlalchemy.Table(
    "public_templates_category",
    metadata,
    sqlalchemy.Column("template_id", sqlalchemy.Integer, ForeignKey("public_templates.template_id"), nullable=False),
    sqlalchemy.Column("category_id", sqlalchemy.Integer, ForeignKey("public_category.category_id"), nullable=False),
    sqlalchemy.PrimaryKeyConstraint("template_id", "category_id", name="public_templates_category_pk")    
)