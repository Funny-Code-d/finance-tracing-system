
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from db.base import database
from endpoints import users, token, group




tags_metadata = [
    {
        "name" : "token",
        "description" : "В данном разделе реализован функционал работы с токеном: создание, рефреш, удаление."
    },
    {
        "name" : "users",
        "description" : "В данном разделе реализован функционал работы с ресурсом пользователь: создание, удаление, полное обновление, частичное обновление, получение записи пользователя по разным ключам."
    }
]


app = FastAPI(
    title="Информационая система контроля личных расходов (API)",
    version='0.0.3',
    openapi_tags=tags_metadata
)



app.include_router(token.route, prefix='/api/token', tags=['token'])
app.include_router(users.route, prefix='/api/{token}/user', tags=['users'])
app.include_router(group.route, prefix='/api/{token}/group', tags=['group'])

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <h1>REST API информационной системы учёта расходов</h1>
    <p>Owner by Sosnin Denis</p>
    <p><a href='/docs/'>Docs</a></p>
    """

# @app.get("/api/{token}/users/")
# async def root(token: str):
#         return {
#         "message": "Hello World",
#         "token" : token
#         }

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True)