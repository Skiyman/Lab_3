from pydantic import BaseModel


class ErrorModel(BaseModel):
    error_message: str


class SuccessMessage(BaseModel):
    status: bool
