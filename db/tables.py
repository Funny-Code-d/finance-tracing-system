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
    sqlalchemy.Column("email", sqlalchemy.String(30), nullable=False),
    sqlalchemy.Column("application", sqlalchemy.String(10)),
    sqlalchemy.Column("date_create", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("date_end_token", sqlalchemy.Date, nullable=False)
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
                      server_default=Sequence("category_id_seq").next_value(), unique=True, nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("customers.user_id"), nullable=False),
    sqlalchemy.Column("name_category", sqlalchemy.String(30), nullable=False),
    sqlalchemy.PrimaryKeyConstraint("user_id", "name_category", name='category_pk')
)

personal_view = sqlalchemy.Table(
    "personal_view",
    metadata,
    sqlalchemy.Column("view_id", sqlalchemy.Integer, Sequence("view_id_seq"),
                      server_default=Sequence("view_id_seq").next_value(), unique=True, nullable=False),
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

