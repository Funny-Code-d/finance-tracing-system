from sqlalchemy import ForeignKey, Column
from sqlalchemy import String, Integer, Text, Boolean, Float, DateTime, TIMESTAMP
from .base import DecBase
from datetime import datetime


class s_token(DecBase):
    __tablename__ = 's_token'
    token_sk = Column(
        Integer,
        ForeignKey("h_token.token_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    name_owner = Column(String, nullable=True)
    email_owner = Column(String, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class s_customer(DecBase):
    __tablename__ = 's_customer'
    customer_sk = Column(
        Integer,
        ForeignKey("h_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class s_group(DecBase):
    __tablename__ = 's_group'
    group_sk = Column(
        String,
        ForeignKey("h_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    name_group = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class s_debtor(DecBase):
    __tablename__ = 's_debtor'
    debtor_sk = Column(
        Integer,
        ForeignKey("h_debtor.debtor_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class s_debtbook_history(DecBase):
    __tablename__ = 's_debtbook_history'
    debtbook_history_sk = Column(Integer, primary_key=True, autoincrement=True)
    debtbook_sk = Column(Integer, ForeignKey("h_debtbook.debtbook_sk", ondelete="CASCADE", onupdate="CASCADE"))
    action = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class s_item_todo_list(DecBase):
    __tablename__ = 's_item_todo_list'
    todo_list_sk = Column(
        Integer,
        ForeignKey("h_todo_list.todo_list_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    item_todo_list_sk = Column(Integer, primary_key=True, autoincrement=True)
    name_item = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=True)
    completed = Column(Boolean, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class s_purchase(DecBase):
    __tablename__ = 's_purchase'
    purchase_sk = Column(
        Integer,
        ForeignKey("h_purchase.purchase_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    total_amount = Column(Float, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class s_purchase_detail(DecBase):
    __tablename__ = 's_purchase_detail'
    purchase_detail_sk = Column(Integer, primary_key=True, autoincrement=True)
    purchase_sk = Column(
        Integer,
        ForeignKey("h_purchase.purchase_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    name_product = Column(String, nullable=False)
    amount = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class s_friends(DecBase):
    __tablename__ = 's_friends'
    customer1_sk = Column(
        Integer,
        ForeignKey("h_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    customer2_sk = Column(
        Integer,
        ForeignKey("h_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    status = Column(Integer, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)
