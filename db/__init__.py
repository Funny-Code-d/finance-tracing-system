from .token import token_table
from .customer import customers
from .debtbook import debt_person, debtbook_table, debtbook_history
from .private_cost import personal_group, personal_category, personal_purchase, detail_personal_purchase, personal_temlates, personal_templates_category
from .public_cost import public_group, public_group_users, public_category, public_purchase, detail_public_purchase, public_templates, public_templates_category

from .base import metadata, engine



metadata.create_all(bind=engine)
# metadata.drop_all(bind=engine)
# 

