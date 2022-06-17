from orm.token_map import TokenEntity
from orm.user_map import UserEntity
from orm.group_map import GroupEntity
from orm.purchase_map import PurchaseEntity
from orm.category_map import CategoryEntity
from orm.templates_map import TemplatesEntity
from orm.todolist_map import ToDoListEntity
from orm.debtbook_map import DebtbookEntity

from repository.users import UserRepository
from repository.token import TokenRepository
from repository.group import GroupRepository
from repository.purchase import PurchaseRepository
from repository.category import CategoryRepository
from repository.templates import TemplatesRepositry
from repository.todolist import TodoListRepositry
from repository.debtbook import DebtorRepository


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


# Purchase
def get_purchase_orm() -> PurchaseEntity:
    return PurchaseEntity()

def get_purchase_repositories() -> PurchaseRepository:
    return PurchaseRepository(get_purchase_orm())
#-----

# Category
def get_category_orm() -> CategoryEntity:
    return CategoryEntity()

def get_category_repositories() -> CategoryRepository:
    return CategoryRepository(CategoryEntity())
#-----

# Templates
def get_templates_orm() -> TemplatesEntity:
    return TemplatesEntity()

def get_templates_repositories() -> TemplatesRepositry:
    return TemplatesRepositry(TemplatesEntity())
#-----

# ToDoList
def get_todolist_orm() -> ToDoListEntity:
    return ToDoListEntity()

def get_todolist_repositories() -> TodoListRepositry:
    return TodoListRepositry(ToDoListEntity())
#-----

# Debtbook
def get_debtbook_orm() -> DebtbookEntity:
    return DebtbookEntity()

def get_debtbook_repositories() -> DebtorRepository:
    return DebtorRepository(DebtbookEntity())
#-----