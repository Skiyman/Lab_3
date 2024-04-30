from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert, update, delete
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
async def get_car(car_id: int) -> CarModel | ErrorModel:
    async with make_session() as session:
        try:
            request = await session.execute(select(Car).where(Car.id == car_id))
            await session.commit()
            return request.scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Автомобиль не найден")


@car_router.post("")
async def create_car(car: CarCreateModel) -> CarModel:
    async with make_session() as session:
        car = Car(**car.model_dump())
        session.add(car)
        await session.commit()
        return await get_car(car_id=car.id)


@car_router.put("/{car_id}")
async def update_car(car_id: int, car: CarCreateModel) -> CarModel | ErrorModel:
    async with make_session() as session:
        request = await session.execute(update(Car).where(Car.id == car_id).values(**car.model_dump()))
        await session.commit()
        return await get_car(car_id)


@car_router.patch("/{car_id}")
async def patch_car(car_id: int, car: CarUpdateModel):
    async with make_session() as session:
        try:
            request = await session.execute(update(Car).where(Car.id == car_id).values(**car.get_values()))
            await session.commit()

            return await get_car(car_id)
        except IntegrityError:
            return ErrorModel(error_message="Производителя не существует")


@car_router.delete("/{car_id}")
async def delete_car(car_id: int) -> SuccessMessage | ErrorModel:
    async with make_session() as session:
        request = await session.execute(delete(Car).where(Car.id == car_id))

        try:
            await session.commit()

            return SuccessMessage(status=200)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Автомобиль не найден")
