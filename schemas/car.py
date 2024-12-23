from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.garage import ResponseGarageDTO


class CreateCarDTO(BaseModel):
    make: str
    model: str
    productionYear:int  # Expected in "yyyy-mm-dd" format
    licensePlate: str
    garageIds: List[int]

    class Config:
        from_attributes = True


class ResponseCarDTO(CreateCarDTO):
    id: int
    make: str
    model: str
    productionYear: int
    licensePlate: str
    garages: List[ResponseGarageDTO]

    class Config:
        from_attributes = True

class UpdateCarDTO(BaseModel):
    make: Optional[str]
    model: Optional[str]
    productionYear: Optional[int]  # It should be an integer, not a string
    licensePlate: Optional[str]  # Optional field to allow for updating
    garageIds: Optional[List[int]] = None



class Config:
        from_attributes = True