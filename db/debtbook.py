from sqlalchemy.schema import Sequence
from sqlalchemy import CheckConstraint, ForeignKey
import sqlalchemy
from .base import metadata


debt_person = sqlalchemy.Table(
    "debt_person",
    metadata,
    sqlalchemy.Column("debtor_id", sqlalchemy.Integer, Sequence("debt_id_seq"), server_default=Sequence("debt_id_seq").next_value(), unique=True, nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("customers.user_id"), nullable=False),
    sqlalchemy.Column("name_debtor", sqlalchemy.String(50), nullable=False),
    sqlalchemy.PrimaryKeyConstraint("user_id", "name_debtor")
)


debtbook_table = sqlalchemy.Table(
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