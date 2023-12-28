import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from db import create_tables
from routers.car import car_router
from routers.manufacturer import manufacturer_router

app = FastAPI()


@app.on_event("startup")
async def on_startup() -> None:
    # Создание таблиц в БД
    await create_tables()


@app.get('/')
async def home() -> dict:
    return {
        "msg": "Hello World!!!"
    }


app.include_router(
    car_router,
)

app.include_router(
    manufacturer_router,
)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)