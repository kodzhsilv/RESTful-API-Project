from pydantic import BaseModel
from datetime import date
from typing import Optional

# Schema for creating or updating a maintenance record
class CreateMaintenanceDTO(BaseModel):
    car_id: int
    service_type: str
    scheduled_date: date
    garage_id: Optional[int]  # Optional, in case the maintenance is not associated with a garage initially

    class Config:
        from_attributes = True

# Schema for the maintenance response
class ResponseMaintenanceDTO(BaseModel):
    id: int
    car_id: int
    car_name: str
    service_type: str
    scheduled_date: date
    garage_id: Optional[int]  # Optional, in case no garage is associated
    garage_name: Optional[str]  # Optional, for when the garage information is available

    class Config:
        from_attributes = True

class UpdateMaintenanceDTO(BaseModel):
    carId: int
    serviceType: str
    scheduledDate: date
    garageId: Optional[int]  # Optional for updates, as it might not always be required to update

    class Config:
        from_attributes = True

class MonthlyRequestReportRequestDTO(BaseModel):
    garageId: int  # The ID of the garage
    startMonth: str  # Start month in 'YYYY-MM' format
    endMonth: str  # End month in 'YYYY-MM' format

    class Config:
        from_attributes = True

class MonthlyRequestReportDTO(BaseModel):
    yearMonth: str  # The year-month for which the report is generated, in 'YYYY-MM' format
    requests: int  # Total requests for the month

    class Config:
        from_attributes = True