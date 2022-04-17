from .hubs import hub_token, hub_customer, hub_group, hub_todo_list, hub_category, hub_templates, hub_purchase, hub_debtor, hun_debtbook
from .settelites import set_token, set_customer, set_group, set_debtor, set_debtbook_history, set_item_todo_list, set_purchase, set_purchase_detail
from .links import link_token_customer, link_customer_debtor, link_debtor_debtbook, link_admin_group, link_pull_group, link_group_todo_list, link_templates_group, link_group_category, link_templates_category, link_purchase_category, link_purcahse_group

from .base import metadata, engine



metadata.create_all(bind=engine)
# metadata.drop_all(bind=engine)
# 

