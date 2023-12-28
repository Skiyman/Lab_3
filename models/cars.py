import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CarCreateModel(BaseModel):
    manufacturer_id: int
    name: str
    production_year: datetime.date


class CarModel(CarCreateModel):
    id: int


class CarUpdateModel(BaseModel):
    manufacturer_id: Optional[int] = Field(None)
    name: Optional[str] = Field(None)
    production_year: Optional[datetime.date] = Field(None)

    def get_values(self):
        return dict((k, v) for k, v in self.model_dump().items() if v is not None)

