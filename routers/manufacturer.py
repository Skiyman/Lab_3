from fastapi import APIRouter
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError, MultipleResultsFound

from db import make_session
from models.manufacturer import ManufacturerModel, ManufacturerCreateModel, ManufacturerUpdateModel
from models.status import ErrorModel, SuccessMessage
from orm.tabels import Manufacturer

manufacturer_router = APIRouter(
    prefix="/manufacturers",
    tags=["Manufacturers"]
)


@manufacturer_router.get("")
async def get_manufacturers() -> list[ManufacturerModel]:
    async with make_session() as session:
        request = await session.execute(select(Manufacturer).order_by(Manufacturer.id))
        result = []

        for manufacturer, in request:
            result.append(manufacturer)

        return result


@manufacturer_router.get("/{manufacturer_id}")
async def get_manufacturer(manufacturer_id: int) -> ManufacturerModel | ErrorModel:
    async with make_session() as session:
        request = await session.execute(select(Manufacturer).where(Manufacturer.id == manufacturer_id))

        try:
            return request.scalar_one()
        except NoResultFound:
            return ErrorModel(error_message="Производителя не существует")


@manufacturer_router.post("")
async def create_manufacturer(manufacturer: ManufacturerCreateModel) -> ManufacturerModel:
    async with make_session() as session:
        manufacturer = Manufacturer(**manufacturer.model_dump())
        session.add(manufacturer)
        await session.commit()

        return await get_manufacturer(manufacturer_id=manufacturer.id)


@manufacturer_router.put("{manufacturer_id}")
async def update_manufacturer(manufacturer_id: int,
                              manufacturer: ManufacturerCreateModel) -> ManufacturerModel | ErrorModel:
    async with make_session() as session:
        request = await session.execute(
            update(Manufacturer).where(Manufacturer.id == manufacturer_id).values(**manufacturer.model_dump()))
        await session.commit()

        return await get_manufacturer(manufacturer_id)


@manufacturer_router.patch("/{manufacturer_id}")
async def patch_manufacturer(manufacturer_id: int,
                             manufacturer: ManufacturerUpdateModel) -> ManufacturerModel | ErrorModel:
    async with make_session() as session:
        request = await session.execute(update(Manufacturer).where(Manufacturer.id == manufacturer_id)
                                .values(**manufacturer.get_values()))
        await session.commit()

        return await get_manufacturer(manufacturer_id)


@manufacturer_router.delete("/{manufacturer_id}")
async def delete_manufacturer(manufacturer_id: int) -> SuccessMessage | ErrorModel:
    async with make_session() as session:
        try:
            request = await session.execute(delete(Manufacturer).where(Manufacturer.id == manufacturer_id))
            await session.commit()

            return SuccessMessage(status=200)
        except NoResultFound:
            return ErrorModel(error_message="Производитель не найден")
        except IntegrityError:
            return ErrorModel(error_message="Производитель уже привязан к какому-либо автомобилю")
