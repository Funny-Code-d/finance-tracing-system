from db.base import database
from repository.users import UserRepository
from repository.token import TokenRepository

def get_user_repository() -> UserRepository:
    return UserRepository(database)

def get_token_repositories() -> TokenRepository:
    return TokenRepository(database)