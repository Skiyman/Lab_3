import uvicorn

from fastapi import FastAPI

from db import run_migrations
from routers.car import car_router
from routers.manufacturer import manufacturer_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    run_migrations()

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
