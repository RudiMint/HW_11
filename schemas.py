from typing import Optional

from pydantic import BaseModel, Field


class ContactSchema(BaseModel):
    first_name: str = Field(max_length=50, min_length=3)
    last_name: str = Field(max_length=50, min_length=3)
    email: str = Field(max_length=50, min_length=5)
    phone: str = Field(max_length=50, min_length=3)
    born_date: str = Field(max_length=30, min_length=8)
    description: Optional[bool] = False


class ContactUpdateSchema(ContactSchema):
    description: bool


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: str
    phone: str
    born_date: str
    description: bool

    class Config:
        from_attributes = True
