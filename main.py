from uvicorn import run as  run_uviorn
from loguru import logger
from fastapi import FastAPI
from fastapi.responses import HTMLResponse



# from endpoints import users, group, purchase, category, templates, todolist, debtbook
from endpoints.token import route as token_route
from endpoints.users import route as user_route
from endpoints.group import route as group_route
from endpoints.category import route as category_route
from endpoints.templates import route as templates_route

from db.create_db import DecBase, Engine



tags_metadata = [
    {
        "name" : "token",
        "description" : "В данном разделе реализован функционал работы с ресурсом токен."
    },
    {
        "name" : "users",
        "description" : "В данном разделе реализован функционал работы с ресурсом пользователь."
    },
    {
        "name" : "group",
        "description" : "В данном разделе реализован функционал работа с ресурсом группа."
    },
    {
        "name" : "category",
        "description" : "В данном разделе реализован функционал работа с категории."
    },
    {
        "name" : "purchase",
        "description" : "В данном разделе реализован функционал работа с ресурсом покупки."
    },
    {
        "name" : "templates",
        "description" : "В данном разделе реализован функционал работа с ресурсом шаблоны отчетов."
    },
    {
        "name" : "todolist",
        "description" : "В данном разделе реализован функционал работа с ресурсом списки запланированных покупок."
    },
    {
        "name" : "debtbook",
        "description" : "В данном разделе реализован функционал работа с ресурсом книга учета долгов."
    }
]


app = FastAPI(
    title="Информационная система контроля личных расходов (API)",
    version='0.1.0',
    openapi_tags=tags_metadata
)


logger.add(
        "logs/Report.log",
        format='{time} | {level} | {message}',
        level="DEBUG",
        rotation="2 MB",
        compression='zip'
    )

app.include_router(token_route, prefix='/api/token', tags=['token'])
app.include_router(user_route, prefix='/api/{token}/user', tags=['users'])
app.include_router(group_route, prefix='/api/{token}/group', tags=['group'])
# app.include_router(purchase.route, prefix="/api/{token}/purchase", tags=['purchase'])
app.include_router(category_route, prefix="/api/{token}/group/category", tags=["category"])
app.include_router(templates_route, prefix="/api/{token}/group/templates", tags=["templates"])
# app.include_router(todolist.route, prefix="/api/{token}/group/todo", tags=["todolist"])
# app.include_router(debtbook.route, prefix="/api/{token}/debtbook", tags=["debtbook"])


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", 'r') as file:
        return file.read()


@app.on_event("startup")
async def startup():
    await connect_db()
    logger.info("API successfully start")


@app.on_event("shutdown")
async def shutdown():
    logger.info("API shutdown")


@logger.catch
def run_project():
    run_uviorn("main:app", port=8000, host='0.0.0.0', reload=True)


@logger.catch
async def connect_db():
    DecBase.metadata.create_all(Engine)


if __name__ == "__main__":
    run_project()
