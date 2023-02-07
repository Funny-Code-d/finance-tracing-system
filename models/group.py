from pydantic import BaseModel
from typing import List, Optional


class GroupModel(BaseModel):
    group_sk: Optional[str]
    name_group: str
    access: str
    description: str

#GET request
class GetAllGroupModelRequest(BaseModel):
    token_sk: Optional[int]
    customer_sk: Optional[int]

class GetGroupModelRequest(GetAllGroupModelRequest):
    group_sk: Optional[str]

# GET responce
class GetGroupModelResponce(GroupModel):
    customer_sk: int

class GetAllGroupModelResponce(BaseModel):
    customer_sk: int
    groups: List[GroupModel]

# POST
class PostGroupModel(GroupModel):
    name_group: str
    access: str
    description: str
    user_id: int

    class Config:
        schema_extra = {
            "example" : {
                "name_group" : "my group",
                "access" : "private [or] public",
                "description" : "Description my group",
                "user_id" : 1,
            }
        }

class PostGroupPoolModel(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str
    added_customer_sk: int

class PatchGroupModel(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str
    group_name: Optional[str]
    access: Optional[str]
    description: Optional[str]

class PutGroupModel(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str
    group_name: str
    access: str
    desciption: str


class DeleteGroup(BaseModel):
    token_sk: Optional[int]
    customer_sk: int
    group_sk: str