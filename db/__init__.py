from .tables import token, customers, category, personal_view, settings_view, purchase, details_purchase
# from .tables import customers
from .base import metadata, engine

metadata.create_all(bind=engine)
# metadata.drop_all(bind=engine)
# 

