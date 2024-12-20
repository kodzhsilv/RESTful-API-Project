from pydantic import BaseModel
from typing import Optional
from datetime import date

# Schema for creating or updating a garage
class CreateGarageDTO(BaseModel):
    name: str
    location: str
    city: str
    capacity: int

    class Config:
        from_attributes = True

# Schema for the garage response
class ResponseGarageDTO(BaseModel):
    id: int
    name: str
    location: str
    city: str
    capacity: int

    class Config:
        from_attributes = True

class UpdateGarageDTO(BaseModel):
    name: str
    location: str
    city: str
    capacity: int

    class Config:
        from_attributes = True

class GarageDailyAvailabilityRequestDTO(BaseModel):
    garageId: int  # The ID of the garage
    startDate: date  # Start date for the report
    endDate: date  # End date for the report

    class Config:
        from_attributes = True

class GarageDailyAvailabilityReportDTO(BaseModel):
    date: date  # The specific date of the report
    requests: int  # Number of requests (e.g., maintenance or car bookings) on that day
    availableCapacity: int  # Available capacity (slots) in the garage on that day

    class Config:
        from_attributes = True