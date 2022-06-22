
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from db.base import database
from endpoints import users, group, purchase, category, templates, todolist, debtbook




tags_metadata = [
    {
        "name" : "users",
        "description" : "В данном разделе реализован функционал работы с ресурсом пользователь."
    },
    {
        "name" : "group",
        "description" : "В данном разделе реализован функционал работа с ресурсом группа."
    },
    {
        "name" : "purchase",
        "description" : "В данном разделе реализован функционал работа с ресурсом покупки."
    },
    {
        "name" : "category",
        "description" : "В данном разделе реализован функционал работа с категории."
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
    title="Информационая система контроля личных расходов (API)",
    version='0.0.3',
    openapi_tags=tags_metadata
)




app.include_router(users.route, prefix='/api/{token}/user', tags=['users'])
app.include_router(group.route, prefix='/api/{token}/group', tags=['group'])
app.include_router(purchase.route, prefix="/api/{token}/purchase", tags=['purchase'])
app.include_router(category.route, prefix="/api/{token}/group/category", tags=["category"])
app.include_router(templates.route, prefix="/api/{token}/group/templates", tags=["templates"])
app.include_router(todolist.route, prefix="/api/{token}/group/todo", tags=["todolist"])
app.include_router(debtbook.route, prefix="/api/{token}/debtbook", tags=["debtbook"])

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", 'r') as file:
        return file.read()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=False)
