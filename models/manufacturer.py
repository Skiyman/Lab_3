from typing import Optional

from pydantic import BaseModel, Field


class ManufacturerCreateModel(BaseModel):
    name: str
    country: str


class ManufacturerModel(ManufacturerCreateModel):
    id: int


class ManufacturerUpdateModel(BaseModel):
    name: Optional[str] = Field(None)
    country: Optional[str] = Field(None)

    def get_values(self):
        return dict((k, v) for k, v in self.model_dump().items() if v is not None)

