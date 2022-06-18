from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.todolist import ToDoListIn, GetToDoList, GetToDoListById, DeleteToDoList, DeleteItemToDoList, ToDoListItemIn
from repository.todolist import TodoListRepositry
from .depends import get_todolist_repositories, get_token_repositories

route = APIRouter()

# @route.get("/", status_code=200)
# async def get_by_id_to_do_list(
#     token: str,
#     customer_sk: int,
#     todo_list_sk: int,
#     group_sk: str,
#     todolist_repositories: TodoListRepositry = Depends(get_todolist_repositories),
#     token_repositories: TokenRepository = Depends(get_token_repositories)):
    
#     token_sk = await token_repositories.verify_access_token(token)
#     todolist_data = GetToDoListById(
#         token_sk=token_sk,
#         customer_sk=customer_sk,
#         group_sk=group_sk,
#         todo_list_sk=todo_list_sk
#     )
#     return await todolist_repositories.get_by_id(todolist_data)


@route.post("/", status_code=204)
async def add_to_do_list(
    token: str,
    todolist_data: ToDoListIn,
    todolist_repositories: TodoListRepositry = Depends(get_todolist_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    todolist_data.token_sk = token_sk
    print(todolist_data)
    return await todolist_repositories.add_todo_list(todolist_data)

@route.post("/item", status_code=204)
async def add_item_to_do_list(
    token: str,
    todolist_data: ToDoListItemIn,
    todolist_repositories: TodoListRepositry = Depends(get_todolist_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    todolist_data.token_sk = token_sk
    print(todolist_data)
    return await todolist_repositories.add_item_todo_list(todolist_data)

@route.get("/", status_code=200)
async def get_all(
    token: str,
    customer_sk: int,
    group_sk: str,
    todolist_repositories: TodoListRepositry = Depends(get_todolist_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    todolist_data = GetToDoList(
        token_sk=token_sk,
        customer_sk=customer_sk,
        group_sk=group_sk
    )
    return await todolist_repositories.get_all(todolist_data)

@route.delete("/", status_code=204)
async def delete_to_do_list(
    token: str,
    todolist_data: DeleteToDoList,
    todolist_repositories: TodoListRepositry = Depends(get_todolist_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    todolist_data.token_sk = token_sk
    return await todolist_repositories.delete_todo_list(todolist_data)

@route.delete("/item", status_code=204)
async def delete_item_to_do_list(
    token: str,
    todolist_data: DeleteItemToDoList,
    todolist_repositories: TodoListRepositry = Depends(get_todolist_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    todolist_data.token_sk = token_sk
    return await todolist_repositories.delete_item_todo_list(todolist_data)

@route.post("/item/complited", status_code=204)
async def complited_item_to_do_list(
token: str,
    todolist_data: DeleteItemToDoList,
    todolist_repositories: TodoListRepositry = Depends(get_todolist_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    todolist_data.token_sk = token_sk
    return await todolist_repositories.complited_item(todolist_data)