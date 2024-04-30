from fastapi import APIRouter, Response
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
async def get_manufacturer(manufacturer_id: int, response: Response) -> ManufacturerModel | ErrorModel:
    async with make_session() as session:
        request = await session.execute(select(Manufacturer).where(Manufacturer.id == manufacturer_id))
        try:
            return request.scalar_one()
        except NoResultFound:
            response.status_code = 404
            return ErrorModel(error_message="Manufacturer doesn't exist")


@manufacturer_router.post("")
async def create_manufacturer(manufacturer: ManufacturerCreateModel, response: Response) -> ManufacturerModel:
    async with make_session() as session:
        manufacturer = Manufacturer(**manufacturer.model_dump())
        session.add(manufacturer)
        await session.commit()

    return await get_manufacturer(manufacturer.id, response)


@manufacturer_router.put("{manufacturer_id}")
async def update_manufacturer(manufacturer_id: int,
                              manufacturer: ManufacturerCreateModel,
                              response: Response) -> ManufacturerModel | ErrorModel:
    async with make_session() as session:
        request = await session.execute(
            update(Manufacturer).where(Manufacturer.id == manufacturer_id).values(**manufacturer.model_dump()))
        await session.commit()

    return await get_manufacturer(manufacturer_id, response)


@manufacturer_router.patch("/{manufacturer_id}")
async def patch_manufacturer(manufacturer_id: int,
                             manufacturer: ManufacturerUpdateModel,
                             response: Response) -> ManufacturerModel | ErrorModel:
    async with make_session() as session:
        request = await session.execute(update(Manufacturer).where(Manufacturer.id == manufacturer_id)
                                        .values(**manufacturer.get_values()))
        await session.commit()

        return await get_manufacturer(manufacturer_id, response)


@manufacturer_router.delete("/{manufacturer_id}")
async def delete_manufacturer(manufacturer_id: int, response: Response) -> SuccessMessage | ErrorModel:
    async with make_session() as session:
        try:
            request = await session.execute(delete(Manufacturer).where(Manufacturer.id == manufacturer_id))
            await session.commit()

            return SuccessMessage(status=200)
        except NoResultFound:
            response.status_code = 404
            return ErrorModel(error_message="Manufacturer doesn't exist")
        except IntegrityError:
            response.status_code = 400
            return ErrorModel(error_message="The manufacturer is already tied to a car")
