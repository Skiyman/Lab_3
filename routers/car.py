

from fastapi import APIRouter, Response
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from db import make_session
from models.cars import CarModel, CarCreateModel, CarUpdateModel
from models.status import ErrorModel, SuccessMessage
from orm.tabels import Car

car_router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)


@car_router.get("")
async def get_cars() -> list[CarModel]:
    async with make_session() as session:
        request = await session.execute(select(Car).order_by(Car.id))
        result = []

        for car, in request:
            result.append(car)

    return result


@car_router.get("/{car_id}")
async def get_car(car_id: int, response: Response) -> CarModel | ErrorModel:
    async with make_session() as session:
        try:
            request = await session.execute(select(Car).where(Car.id == car_id))
            await session.commit()
            return request.scalar_one()
        except NoResultFound:
            response.status_code = 404
            return ErrorModel(error_message="Сar doesn't exist")


@car_router.post("")
async def create_car(car: CarCreateModel, response: Response) -> CarModel:
    async with make_session() as session:
        car = Car(**car.model_dump())
        session.add(car)
        await session.commit()
    return await get_car(car.id, response)


@car_router.put("/{car_id}")
async def update_car(car_id: int, car: CarCreateModel, response: Response) -> CarModel | ErrorModel:
    async with make_session() as session:
        request = await session.execute(update(Car).where(Car.id == car_id).values(**car.model_dump()))
        await session.commit()
    return await get_car(car_id, response)


@car_router.patch("/{car_id}")
async def patch_car(car_id: int, car: CarUpdateModel, response: Response):
    async with make_session() as session:
        try:
            request = await session.execute(update(Car).where(Car.id == car_id).values(**car.get_values()))
            await session.commit()

            return await get_car(car_id, response)
        except IntegrityError:
            response.status_code = 400
            return ErrorModel(error_message="Manufacturer doesn't exist")


@car_router.delete("/{car_id}")
async def delete_car(car_id: int) -> SuccessMessage | ErrorModel:
    async with make_session() as session:
        request = await session.execute(delete(Car).where(Car.id == car_id))
        await session.commit()
        return SuccessMessage(status=200)
