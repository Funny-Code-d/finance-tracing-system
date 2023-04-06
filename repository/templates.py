from fastapi import Response, status, HTTPException
from sqlalchemy import text


from .base import BaseRepository
from models.templates import GetGeneralStatistics, GetReport, TemplatesIn, GetTemplates, DeleteTemplate, PatchTemplate
from modules.tokens import access_control, access_group
from db.hubs import h_templates
from db.links import l_templates_category, l_templates_group
from db.base import Engine


class TemplatesRepositry(BaseRepository):
    
    @access_control
    @access_group
    async def create(self, name_template, number_days, categoies, customer_sk, group_sk, token):

        hub = h_templates(
            name_template=name_template,
            number_days=number_days
        )
        self.session.add(hub)
        self.session.commit()

        link_group = l_templates_group(
            template_sk=hub.template_sk,
            group_sk=group_sk
        )
        self.session.add(link_group)

        for category_sk in categoies:
            link_category = l_templates_category(
                template_sk=hub.template_sk,
                category_sk=category_sk
            )
            self.session.add(link_category)

        self.session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
        


    @access_control
    @access_group
    async def get_all(self, customer_sk, group_sk, token):
        
        query = f"""
            SELECT t1.template_sk, t1.name_template, t1.number_days
                FROM h_templates t1
                JOIN l_templates_group t2 ON t1.template_sk=t2.template_sk
                WHERE t2.group_sk = '{group_sk}'
        """

        with Engine.connect() as conn:
            list_templates = list()
            result = conn.execute(text(query))

            for item in result:
                # categories = self.session.query(l_templates_category).filter(l_templates_category.template_sk == item[0]).all()
                query = f"""
                    SELECT t2.category_sk, t2.name_category
                        FROM l_templates_category t1
                        JOIN h_category t2 ON t1.category_sk=t2.category_sk
                        WHERE t1.template_sk = {item[0]}
                """
                categories = conn.execute(text(query))
                list_categories = list()
                for item_category in categories:
                    list_categories.append({
                        "category_sk": item_category[0],
                        "name_category": item_category[1]
                    })
                list_templates.append({
                    "template_sk": item[0],
                    "name_template": item[1],
                    "number_days": item[2],
                    "categories": list_categories
                })

        return list_templates 

    
    async def delete_template(self, template_sk, customer_sk, group_sk, token):
        
        hub = self.session.query(h_templates).filter(h_templates.template_sk == template_sk).first()

        link_group = self.session.query(l_templates_group).filter(l_templates_group.template_sk == template_sk).first()

        link_categories = self.session.query(l_templates_category).filter(l_templates_category.template_sk == template_sk).all()

        for item in link_categories:
            self.session.delete(item)
        
        self.session.delete(link_group)
        self.session.commit()

        self.session.delete(hub)

        return Response(status_code=status.HTTP_200_OK)
        
    async def patch_template(self, template_sk, customer_sk, group_sk, token, name_template=None, number_days=None):
        pass
        
    
    async def get_general_statistics(self, template_sk, customer_sk, group_sk, token):
        pass
        
        
    async def get_general_statistics_detail(self, template_sk, customer_sk, group_sk, token):
        pass
    
    