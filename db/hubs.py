from sqlalchemy import Column
from sqlalchemy import String, Integer, Text, Boolean, Float, DateTime, TIMESTAMP
from .base import DecBase
from datetime import datetime


class h_token(DecBase):
    __tablename__ = 'h_token'
    token_sk = Column(Integer, primary_key=True, autoincrement=True)
    access_token = Column(Text, unique=True, nullable=False)
    refresh_token = Column(Text, unique=True, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class h_customer(DecBase):
    __tablename__ = 'h_customer'
    customer_sk = Column(Integer, unique=True, autoincrement=True, primary_key=True)
    email = Column(String, unique=True)
    telegram_id = Column(Integer, unique=True, nullable=True)
    password = Column(Text, nullable=True)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class h_group(DecBase):
    __tablename__ = 'h_group'
    group_sk = Column(String, primary_key=True)
    access = Column(String, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class h_todo_list(DecBase):
    __tablename__ = 'h_todo_list'
    todo_list_sk = Column(Integer, primary_key=True, autoincrement=True)
    name_todo_list = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class h_category(DecBase):
    __tablename__ = 'h_category'
    category_sk = Column(Integer, primary_key=True, autoincrement=True)
    name_category = Column(String, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class h_templates(DecBase):
    __tablename__ = 'h_templates'
    template_sk = Column(Integer, primary_key=True, autoincrement=True)
    name_template = Column(String, nullable=False)
    number_days = Column(Integer, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class h_purchase(DecBase):
    __tablename__ = 'h_purchase'
    purchase_sk = Column(Integer, primary_key=True, autoincrement=True)
    name_store = Column(String, nullable=True)
    date_purchase = Column(DateTime, nullable=False, default=datetime.utcnow)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


# class h_debtor(DecBase):
#     __tablename__ = 'h_debtor'
#     debtor_sk = Column(Integer, primary_key=True, autoincrement=True)
#     debtor_name = Column(String, nullable=False)
#     load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class h_debtbook(DecBase):
    __tablename__ = 'h_debtbook'
    debtbook_sk = Column(Integer, primary_key=True, autoincrement=True)
    debtor_name = Column(String, nullable=False)
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)
