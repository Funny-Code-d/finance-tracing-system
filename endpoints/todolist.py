from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.todolist import ToDoListIn
from repository.todolist import TodoListRepositry
from .depends import get_todolist_repositories, get_token_repositories

route = APIRouter()

@route.post("/", status_code=200)
async def add_to_do_list(
    token: str,
    todolist_data: ToDoListIn,
    todolist_repositories: TodoListRepositry = Depends(get_todolist_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    todolist_data.token_sk = token_sk
    print(todolist_data)
    return await todolist_repositories.add_template(todolist_data)

# @route.post("/refresh", status_code=200)
# async def refresh_token(
#     token: TokenAuthIn,
#     tokens: TokenRepository = Depends(get_purchase_repositories)):
    
#     responce = await tokens.refresh_token(token)

#     if responce is False:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token did not pass the auth")
#     else:
#         return responce

# @route.delete("/", status_code=204)
# async def delete_token(
#     token: TokenDelete,
#     tokens: TokenRepository = Depends(get_purchase_repositories)):

#     responce = await tokens.delete_token(token=token)

#     if responce:
#         return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="token was delete")
#     else:
#         return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token did not pass the auth")