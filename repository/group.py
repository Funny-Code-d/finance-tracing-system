from fastapi import Response, status, HTTPException
from sqlalchemy import text

from modules.tokens import access_control
from .base import BaseRepository
from db.hubs import h_group, h_customer
from db.sattelites import s_group
from db.links import l_admin_group, l_pull_group
from models.group import PatchGroupModel, PostGroupModel, GetGroupModelRequest, GetAllGroupModelRequest, PutGroupModel, DeleteGroup
from db.base import Engine


class GroupRepository(BaseRepository):

    async def check_link_token_group(self, token, group_id):
        query = f"""
            select t1.group_sk from h_group t1
                join l_admin_group t2 on t1.group_sk=t2.group_sk
                join h_customer t3 on t2.customer_sk=t3.customer_sk
                join l_token_customer t4 on t3.customer_sk=t4.customer_sk
                join h_token t5 on t4.token_sk=t5.token_sk
                    where t5.access_token = '{token}' and
                    t1.group_sk = '{group_id}'
        """
        with Engine.connect() as conn:
            result = conn.execute(text(query)).fetchone()
            if result is None:
                return False
            else:
                return True

    @access_control
    async def create_group(self, group: PostGroupModel, token):

        group_sk = group.name_group + str(group.user_id)

        hub = h_group(
            group_sk=group_sk,
            access=group.access
        )
        self.session.add(hub)
        self.session.commit()

        sat = s_group(
            group_sk=group_sk,
            name_group=group.name_group,
            description=group.name_group
        )

        link_admin = l_admin_group(
            customer_sk=group.user_id,
            group_sk=group_sk
        )

        link_pull = l_pull_group(
            customer_sk=group.user_id,
            group_sk=group_sk
        )

        self.session.add(sat)
        self.session.add(link_admin)
        self.session.add(link_pull)
        self.session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @access_control
    async def get_by_id(self, group_id, token):
        is_valid = self.check_link_token_group(token, group_id)
        if is_valid:
            hub = self.session.query(h_group).filter(h_group.group_sk == group_id).first()
            sat = self.session.query(s_group).filter(s_group.group_sk == group_id).first()

            pull_list = list()
            query = f"""
                select t3.customer_sk, t3.first_name, t3.last_name from l_pull_group t1
                    join h_customer t2 on t1.customer_sk=t2.customer_sk
                    join s_customer t3 on t2.customer_sk=t3.customer_sk
                        where t1.group_sk = '{group_id}'
            """
            with Engine.connect() as conn:
                result_from_db = conn.execute(text(query))
                for item in result_from_db:
                    pull_list.append({
                        "customer_sk": item['customer_sk'],
                        "first_name": item['first_name'],
                        "last_name": item['last_name']
                    })
            if hub:
                return {
                    "group_id": hub.group_sk,
                    "name_group": sat.name_group,
                    "access": hub.access,
                    "description": sat.description,
                    "pull": pull_list
                }
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="the group does not belong to your token")

    @access_control
    async def get_list(self, user_id, token):
        query = f"""
            select t1.*, t6.* from h_group t1
                join l_admin_group t2 on t1.group_sk=t2.group_sk
                join h_customer t3 on t2.customer_sk=t3.customer_sk
                join l_token_customer t4 on t3.customer_sk=t4.customer_sk
                join h_token t5 on t4.token_sk=t5.token_sk
                join s_group t6 on t6.group_sk=t1.group_sk
                    where t5.access_token = '{token}' and
                    t3.customer_sk = '{user_id}'
        """

        with Engine.connect() as conn:
            result_from_db = conn.execute(text(query))
            result_list = list()
            for item in result_from_db:

                pull_list = list()
                query = f"""
                select t3.customer_sk, t3.first_name, t3.last_name from l_pull_group t1
                    join h_customer t2 on t1.customer_sk=t2.customer_sk
                    join s_customer t3 on t2.customer_sk=t3.customer_sk
                        where t1.group_sk = '{item['group_sk']}'
                """

                result_from_db = conn.execute(text(query))
                for item_pull in result_from_db:
                    pull_list.append({
                        "customer_sk": item_pull['customer_sk'],
                        "first_name": item_pull['first_name'],
                        "last_name": item_pull['last_name']
                    })

                result_list.append({
                    "group_id": item['group_sk'],
                    "name_group": item['name_group'],
                    "access": item['access'],
                    "description": item['description'],
                    "pull": pull_list
                })
        return {
            "user_id": user_id,
            "groups": result_list
        }

    # @access_control
    # async def put(self, group: PutGroupModel):
    #     is_valid = await self.db_orm.check_token_customer(group.token_sk, group.customer_sk)
    #     if is_valid:
    #         responce_db = await self.db_orm.update(group=group)
    #         if responce_db:
    #             return Response(status_code=status.HTTP_204_NO_CONTENT)
    #         else:
    #             return False
    #     else:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="the group does not belong to your token")
    #
    # @access_control
    # async def patch(self, group: PatchGroupModel):
    #     print(group.token_sk, group.customer_sk)
    #     is_valid = await self.db_orm.check_token_customer(group.token_sk, group.customer_sk)
    #     print(is_valid)
    #     if is_valid:
    #         responce_db = await self.db_orm.update(group=group)
    #         if responce_db:
    #             return Response(status_code=status.HTTP_204_NO_CONTENT)
    #         else:
    #             return False
    #     else:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="the group does not belong to your token")
    #
    # @access_control
    # async def delete(self, group: DeleteGroup):
    #     is_valid = await self.db_orm.check_token_customer(group.token_sk, group.customer_sk)
    #     if is_valid:
    #         responce_db = await self.db_orm.delete(group.group_sk)
    #         if responce_db:
    #             return Response(status_code=status.HTTP_204_NO_CONTENT)
    #         else:
    #             return False
    #     else:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="the group does not belong to your token")