from sqlalchemy.schema import Sequence
from sqlalchemy import CheckConstraint, ForeignKey
import sqlalchemy
from .base import metadata


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