
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()



@app.get("/", response_class=HTMLResponse)
def index():
    return "<h1>REST API информационной системы учёта расходов</h1><p>Owner by Sosnin Denis</p>"

@app.get("/api/{token}/users/")
async def root(token: str):
        return {
        "message": "Hello World",
        "token" : token
        }
