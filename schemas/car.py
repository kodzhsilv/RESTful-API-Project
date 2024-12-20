from pydantic import BaseModel, Field
from typing import Optional


class CreateCarDTO(BaseModel):
    make: str
    model: str
    production_year: str  # Expected in "yyyy-mm-dd" format
    license_plate: str
    garage_id: Optional[int] = Field(None, description="ID of the garage where the car is located")

    class Config:
        from_attributes = True

class ResponseCarDTO(CreateCarDTO):
    id: int
    make: str
    model: str
    productionYear: str
    license_plate: str
    garage_id: Optional[int] = Field(None, description="ID of the garage where the car is located")

    class Config:
        from_attributes = True

class UpdateCarDTO(BaseModel):
    make: Optional[str]
    model: Optional[str]
    productionYear: Optional[str]
    license_plate: str
    garage_id: Optional[int] = Field(None, description="ID of the garage where the car is located")

    class Config:
        from_attributes = True