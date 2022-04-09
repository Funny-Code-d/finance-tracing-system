from sqlalchemy.schema import Sequence
from sqlalchemy import CheckConstraint, ForeignKey
import sqlalchemy
from .base import metadata



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