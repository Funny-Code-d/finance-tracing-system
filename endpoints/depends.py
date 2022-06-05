from orm.token_map import TokenEntity
from orm.user_map import UserEntity
from orm.group_map import GroupEntity
from repository.users import UserRepository
from repository.token import TokenRepository
from repository.group import GroupRepository

# Token 
def get_token_orm() -> TokenEntity:
    return TokenEntity()

def get_token_repositories() -> TokenRepository:
    return TokenRepository(get_token_orm())
#-----



# User
def get_user_orm() -> UserEntity:
    return UserEntity()

def get_user_repository() -> UserRepository:
    return UserRepository(get_user_orm())
#-----



# Group
def get_group_orm() -> GroupEntity:
    return GroupEntity()

def get_group_repositories() -> GroupRepository:
    return GroupRepository(get_group_orm())
#-----