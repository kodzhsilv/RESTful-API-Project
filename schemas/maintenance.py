from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List


# Schema for creating or updating a maintenance record
class CreateMaintenanceDTO(BaseModel):
    serviceType: str
    scheduledDate: date
    carId: int
    garageId: int
   #service_type: str
   #scheduled_date: date
   #car_id: int
   #garage_id: int
   #car_id: int = Field(..., alias='carId')
   #garage_id: int = Field(..., alias='garageId')
   #service_type: str = Field(..., alias='serviceType')
   #scheduled_date: date= Field(..., alias='scheduledDate')

    class Config:
        from_attributes = True

# Schema for the maintenance response
class ResponseMaintenanceDTO(BaseModel):
    id: int
    carId: int
    carName: str
    garageId: int
    garageName: Optional[str]  # Optional, as the garage name might not be present
    scheduledDate: date
    serviceType: str

    class Config:
        from_attributes = True

class UpdateMaintenanceDTO(BaseModel):
    carId: Optional[int]
    serviceType:  Optional[str]
    scheduledDate:  Optional[date]
    garageId: Optional[int]  # Optional for updates, as it might not always be required to update

    class Config:
        from_attributes = True
class YearMonth(BaseModel):
    year: int  # The year part of the month (e.g., 2021)
    month: int  # The month part (1-12)
    leapYear: bool  # Whether it's a leap year
    monthValue: int  # The number of days in the month (28, 29, 30, 31)

class MonthlyRequestsReportDTO(BaseModel):
    yearMonth: YearMonth  # The year-month for which the report is generated, in 'YYYY-MM' format
    requests: int  # Total requests for the month

    class Config:
        from_attributes = True

class MonthlyMaintenanceReportEntryDTO(BaseModel):
    garageId: int  # ID of the garage (if applicable)
    startMonth: date  # The start month (e.g., "2021-05-01")
    endMonth: date  # The end month (e.g., "2026-12-01")

    class Config:
        from_attribute = True