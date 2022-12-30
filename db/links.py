from sqlalchemy import ForeignKey, Column
from sqlalchemy import String, Integer, TIMESTAMP
from .base import DecBase
from datetime import datetime


class l_token_customer(DecBase):
    __tablename__ = 'l_token_customer'
    token_sk = Column(
        Integer,
        ForeignKey("h_token.token_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    customer_sk = Column(
        Integer,
        ForeignKey("h_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class l_customer_debtor(DecBase):
    __tablename__ = 'l_customer_debtor'
    customer_sk = Column(
        Integer,
        ForeignKey("h_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    debtor_sk = Column(
        Integer,
        ForeignKey("h_debtor.debtor_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class l_debtor_debtbook(DecBase):
    __tablename__ = 'l_debtor_debtbook'
    debtor_sk = Column(
        Integer,
        ForeignKey("h_debtor.debtor_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    debtbook_sk = Column(
        Integer,
        ForeignKey("h_debtbook.debtbook_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class l_admin_group(DecBase):
    __tablename__ = 'l_admin_group'
    customer_sk = Column(
        Integer,
        ForeignKey("h_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    group_sk = Column(
        String,
        ForeignKey("h_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class l_pull_group(DecBase):
    __tablename__ = 'l_pull_group'
    customer_sk = Column(
        Integer,
        ForeignKey("h_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    group_sk = Column(
        Integer,
        ForeignKey("h_customer.customer_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class l_group_todo_list(DecBase):
    __tablename__ = 'l_group_todo_list'
    group_sk = Column(
        String,
        ForeignKey("h_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    todo_list_sk = Column(
        Integer,
        ForeignKey("h_todo_list.todo_list_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class l_templates_group(DecBase):
    __tablename__ = 'l_templates_group'
    template_sk = Column(
        Integer,
        ForeignKey("h_templates.template_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    group_sk = Column(
        String,
        ForeignKey("h_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class l_category_group(DecBase):
    __tablename__ = 'l_category_group'
    category_sk = Column(
        Integer,
        ForeignKey("h_category.category_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    group_sk = Column(
        String,
        ForeignKey("h_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class l_templates_category(DecBase):
    __tablename__ = 'l_templates_category'
    template_sk = Column(
        Integer,
        ForeignKey("h_templates.template_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    category_sk = Column(
        Integer,
        ForeignKey("h_category.category_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class l_purchase_category(DecBase):
    __tablename__ = 'l_purchase_category'
    purchase_sk = Column(
        Integer,
        ForeignKey("h_purchase.purchase_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    category_sk = Column(
        Integer,
        ForeignKey("h_category.category_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)


class l_purchase_group(DecBase):
    __tablename__ = 'l_purchase_group'
    purchase_sk = Column(
        Integer,
        ForeignKey("h_purchase.purchase_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    group_sk = Column(
        String,
        ForeignKey("h_group.group_sk", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    load_dttm = Column(TIMESTAMP, default=datetime.utcnow)
