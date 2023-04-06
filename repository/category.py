from fastapi import Response, status, HTTPException
from sqlalchemy import text

from .base import BaseRepository
from db.hubs import h_category
from db.links import l_category_group
from db.sattelites import s_group
from modules.tokens import access_control, access_group
from db.base import Engine

class CategoryRepository(BaseRepository):
        
    @access_control
    @access_group
    async def create(self, name_category: str, customer_sk: int, group_sk: str, token: str):
        print(name_category)
        hub = h_category(
            name_category=name_category
        )
        self.session.add(hub)
        self.session.commit()

        link = l_category_group(
            category_sk=hub.category_sk,
            group_sk=group_sk
        )
        self.session.add(link)
        self.session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
        

    @access_control
    @access_group
    async def get_all(self, customer_sk: int, group_sk: str, token: str):
        query = f"""
            SELECT t1.category_sk, t1.name_category
                FROM h_category t1
                JOIN l_category_group t2 ON t1.category_sk=t2.category_sk
                WHERE t2.group_sk = '{group_sk}'
        """
        
        with Engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            category_list = list()
            for item in result:
                item_list = {
                    "category_id": item[0],
                    "name_category": item[1]
                }

                category_list.append(item_list)
        group_name = self.session.query(s_group).filter(s_group.group_sk == group_sk).first()   


        try:
            return {
                "group_name": group_name.name_group,
                "categories": category_list
            }
        except AttributeError:
            return {
                "categories": category_list
            }

        
    
    @access_control
    @access_group
    async def delete_category(self, category_sk: int, customer_sk: int, group_sk: str, token: str):
        
        link = self.session.query(l_category_group).filter(l_category_group.category_sk == category_sk).first()
        hub = self.session.query(h_category).filter(h_category.category_sk == category_sk).first()

        self.session.delete(link)
        self.session.commit()
        self.session.delete(hub)
        self.session.commit()
        return Response(status_code=status.HTTP_200_OK)
        
    @access_control
    @access_group
    async def put_category(self, name_category: str, category_sk: int, customer_sk: int, group_sk: str, token: str):
        hub = self.session.query(h_category).filter(h_category.category_sk == category_sk).first()
        hub.name_category = name_category
        self.session.commit()
        return Response(status_code=status.HTTP_200_OK)
    
