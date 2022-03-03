
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from db.base import database
app = FastAPI()



@app.get("/", response_class=HTMLResponse)
async def index():
    return "<h1>REST API информационной системы учёта расходов</h1><p>Owner by Sosnin Denis</p>"

@app.get("/api/{token}/users/")
async def root(token: str):
        return {
        "message": "Hello World",
        "token" : token
        }

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True)