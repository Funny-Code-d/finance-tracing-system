from sqlalchemy import select
from .base import BaseEntity
from db.hubs import hub_templates, hub_category
from db.settelites import set_purchase, set_purchase_detail
from db.links import link_templates_group, link_templates_category
from models.purchase import PurchaseIn, Purchase
from models.templates import TemplatesIn, TemplatesOut, TemplatesOutItem, GetTemplates, DeleteTemplate
from sqlalchemy import select
from pydantic.error_wrappers import ValidationError
from typing import List
from datetime import datetime
from pprint import pprint


class TemplatesEntity(BaseEntity):


    async def add_template(self, template: TemplatesIn):
        values = {
            "name_template" : template.name_template,
            "number_days" : template.number_days,
        }
        query = hub_templates.insert().values(**values)
        template_sk = await self.database.execute(query=query)

        
        values = {
            "template_sk" : template_sk,
            "group_sk" : template.group_sk
        }
        query = link_templates_group.insert().values(**values)
        await self.database.execute(query=query)

        for category in template.categories:
            values = {
                "template_sk" : template_sk,
                "category_sk" : category
            }

            query = link_templates_category.insert().values(**values)
            await self.database.execute(query=query)
        
        return True
        
    

    async def get_all(self, template_data: GetTemplates):
        query = select(
            hub_templates.c.template_sk,
            hub_templates.c.name_template,
            hub_templates.c.number_days,
            hub_category.c.category_sk,
            hub_category.c.name_category
        ).join_from(link_templates_group, hub_templates)
        query = query.join_from(hub_templates, link_templates_category)
        query = query.join_from(link_templates_category, hub_category)
        query = query.where(
            link_templates_group.c.group_sk==template_data.group_sk
        )

        result = dict()
        responce_db = await self.database.fetch_all(query=query)
        for row in responce_db:
            result[row['template_sk']] = {
                "name_template" : None,
                "number_days" : None,
                "categories" : list()
            }

        for row in responce_db:
            result[row['template_sk']]['name_template'] = row['name_template']
            result[row['template_sk']]['number_days'] = row['number_days']
            result[row['template_sk']]['categories'].append({
                "category_sk" : row['category_sk'],
                "name_category" : row['name_category']
            })

        new_result = list()
        for key in result.keys():
            new_result.append(result[key])

        return {
            "customer_sk" : template_data.customer_sk,
            "group_sk" : template_data.group_sk,
            "items" : new_result
        }
        

    # async def put(self, )
                
                

    async def delete_template(self, template_data: DeleteTemplate):
        query = link_templates_group.delete().where(
            link_templates_group.c.template_sk==template_data.template_sk
        )
        await self.database.execute(query=query)

        query = link_templates_category.delete().where(
            link_templates_category.c.template_sk==template_data.template_sk
        )
        await self.database.execute(query=query)

        query = hub_templates.delete().where(
            hub_templates.c.template_sk==template_data.template_sk
        )
        await self.database.execute(query=query)

        return True

    async def get_by_category(self):
        pass

    async def get_by_date_and_category(self):
        pass