from sqlalchemy import select, values
from .base import BaseEntity
from db.hubs import hub_templates, hub_category
from db.settelites import sat_purchase, sat_purchase_detail
from db.links import link_templates_group, link_templates_category, link_purcahse_group, link_purchase_category
from models.purchase import PurchaseIn, Purchase
from models.templates import GetGeneralStatistics, GetReport, TemplatesIn, TemplatesOut, TemplatesOutItem, GetTemplates, DeleteTemplate, PatchTemplate
from sqlalchemy import select
from pydantic.error_wrappers import ValidationError
from typing import List
from datetime import date, timedelta
from pprint import pprint
from db.hubs import hub_purchase




class TemplatesEntity(BaseEntity):


    def clean_model_data(self, target_dict):
        result = dict()
        for key in target_dict.keys():
            if target_dict[key] != None:
                result[key] = target_dict[key]
        return result

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
                "template_sk" : None,
                "name_template" : None,
                "number_days" : None,
                "categories" : list()
            }

        for row in responce_db:
            result[row['template_sk']]['template_sk'] = row['template_sk']
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

    async def patch_template(self, template_data: PatchTemplate):
        
        values = {
            "name_template" : template_data.name_template,
            "number_days" : template_data.number_days
        }

        values = self.clean_model_data(values)

        if len(values) > 0:
            query = hub_templates.update().values(**values).where(
                hub_templates.c.template_sk==template_data.template_sk
            )

            await self.database.execute(query=query)


        if template_data.categories is not None:
            if len(template_data.categories) > 0:
                query = link_templates_category.delete().where(
                    link_templates_category.c.template_sk==template_data.template_sk
                )

                await self.database.execute(query=query)

                for categories in template_data.categories:
                    values = {
                        "template_sk" : template_data.template_sk,
                        "category_sk" : categories
                    }
                    query = link_templates_category.insert().values(**values)
                    await self.database.execute(query=query)

        return True
        

    async def get_general_statistics(self, template_data: GetGeneralStatistics):
        date_start = date.today() - timedelta()
        query = select(
            hub_purchase.c.name_store,
            sat_purchase.c.total_amount,
            sat_purchase.c.date_purcahse
        ).join_from(link_purcahse_group, hub_purchase)
        query = query.join_from(hub_purchase, sat_purchase).where(sat_purchase.c.date_purchase > date_start)

        responce_db = await self.database.fetch_all()
        
        if responce_db:
            result = list()
            for row in responce_db:
                item = {
                    "name_store" : row['name_store'],
                    "total_amount" : row['total_amount'],
                    "date_purchase" : row['date_purchase']
                }
                result.append(item)
            return result
        else:
            return False
        
    
    async def get_general_statistics_detail(self, template_data: GetGeneralStatistics):
        date_start = date.today() - timedelta()
        query = select(
            hub_purchase.c.purchase_sk,
            hub_purchase.c.name_store,
            sat_purchase.c.total_amount,
            sat_purchase.c.date_purchase
        ).join_from(link_purcahse_group, hub_purchase)
        query = query.join_from(hub_purchase, sat_purchase).where(sat_purchase.c.date_purchase > date_start, link_purcahse_group.c.group_sk==template_data.group_sk)

        responce_db = await self.database.fetch_all(query=query)
        
        if responce_db:
            result = list()
            for row in responce_db:

                query = sat_purchase_detail.select().where(sat_purchase_detail.c.purchase_sk==row['purchase_sk'])
                responce_db_item = await self.database.fetch_all(query=query)
                detail_purchase = list()
                for row_item in responce_db_item:
                    detail_purchase.append({
                        "name_product" : row_item['name_product'],
                        "amount" : row_item['amount'],
                        "quantity" : row_item['quantity']
                    })
                item = {
                    "name_store" : row['name_store'],
                    "total_amount" : row['total_amount'],
                    "date_purchase" : row['date_purchase'],
                    "detail" : detail_purchase
                }
                result.append(item)
            return result
        else:
            return False
    

    async def get_templates(self, templates_data: GetReport):

        query = hub_templates.seelect().where(hub_templates.c.template_sk==templates_data.template_sk)

        repsonce_db = await self.database.fetch_one(query=query)
        name_template = responce_db['name_template']
        number_days = repsonce_db['number_days']

        query = link_templates_category.select().where(link_templates_category.c.template_sk==templates_data.template_sk)

        responce_db = await self.database.fetch_all(query=query)
        categories_list = list()
        if len(responce_db) > 0:
            for row in responce_db:
                categories_list.append(row['category_sk'])
        else:
            return (name_template, number_days, categories_list)

        
    async def get_purchase_by_template(self, group_sk, number_days, categories):
        date_start = date.today() - timedelta(number_days)
        query = select(
            hub_purchase.c.purchase_sk,
            hub_purchase.c.name_store).join_from(link_purcahse_group, hub_purchase)
        query = query.join_from(hub_templates, link_purchase_category)
        query = query.where(
            link_purcahse_group.c.group_sk==group_sk,
            hub_purchase.c.date_purchase>=date_start,
            link_purchase_category.c.category_sk.in_(categories)
            )
        print(query)

        responce_db = await self.database.fetch_all(query)

        result = list()
        if len(responce_db) > 0:
            for row in responce_db:
                result.append({
                    "purchase_sk" : row['purchase_sk'],
                    "name_store" : row['purchase_sk']
                })
        
        return result

        # for item in categories:
        #     query = query.where(link_purchase_category.c.)
