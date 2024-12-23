from sqlalchemy import cast, Date
from fastapi import APIRouter, Depends, HTTPException
from datetime import date, datetime
from sqlalchemy.orm import Session, joinedload
import schemas.maintenance
from models.car import Car
from schemas.maintenance import CreateMaintenanceDTO
from config import db
from models.car import Car
from models.garage import Garage
from schemas.maintenance import CreateMaintenanceDTO, ResponseMaintenanceDTO
from schemas.maintenance import MonthlyRequestsReportDTO, UpdateMaintenanceDTO, YearMonth
from services.maintenance_service import MaintenanceService, get_request_count_for_month, is_leap_year, get_month_value
from repositories.maintenance_repository import MaintenanceRepository
from config.db import get_db
from typing import List, cast  # Add this import
from typing import Optional
from fastapi import Query
from sqlalchemy.orm import Session
from schemas.maintenance import ResponseMaintenanceDTO
from models.maintenance import Maintenance

router = APIRouter(prefix="/maintenance", tags=["Maintenances"])


@router.get("", response_model=List[ResponseMaintenanceDTO])
async def list_maintenance(
        carId: Optional[int] = None,
        garageId: Optional[int] = None,
        startDate: Optional[str] = None,
        endDate: Optional[str] = None,
        db: Session = Depends(get_db)
):
    # Start with the base query for all maintenances
    query = db.query(Maintenance)
    if carId:
        query = query.filter(Maintenance.carId == carId)
    if garageId:
        query = query.filter(Maintenance.garageId == garageId)

    if startDate:
        try:
            start_date = datetime.strptime(startDate, "%Y-%m-%d")
            query = query.filter(Maintenance.scheduledDate >= start_date)
        except ValueError:
            print(f"Error parsing startDate: {startDate}")

    if endDate:
        try:
            end_date = datetime.strptime(endDate, "%Y-%m-%d")
            query = query.filter(Maintenance.scheduledDate <= end_date)
        except ValueError:
            print(f"Error parsing endDate: {endDate}")

    maintenance_records = query.all()

    return [
        ResponseMaintenanceDTO(
            id=maintenance.id,
            carId=maintenance.carId,
            carName=maintenance.car.make,  # Assuming 'make' is a column in Car model
            garageId=maintenance.garageId,
            garageName=maintenance.garage.name,  # Assuming 'name' is a column in Garage model
            scheduledDate=maintenance.scheduledDate,
            serviceType=maintenance.serviceType
        )
        for maintenance in maintenance_records
    ]

@router.get("/{maintenance_id}", response_model=ResponseMaintenanceDTO)
def get_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    service = MaintenanceService(MaintenanceRepository(db))
    maintenance = service.get_maintenance(maintenance_id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return maintenance

# Create a new maintenance record
@router.post("", response_model=ResponseMaintenanceDTO)
async def create_maintenance(maintenance: CreateMaintenanceDTO, db: Session = Depends(get_db)):
    db_maintenance = Maintenance(**maintenance.dict())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)

    # Assuming db_maintenance has relationships with `car` and `garage`
    return ResponseMaintenanceDTO(
        id=db_maintenance.id,
        serviceType=db_maintenance.serviceType,
        scheduledDate=db_maintenance.scheduledDate,
        carId=db_maintenance.carId,  # Assuming you have a foreign key to `car`
        garageId=db_maintenance.garageId,  # Assuming you have a foreign key to `garage`
        carName=db_maintenance.car.make,  # Access the related car's `name`
        garageName=db_maintenance.garage.name  # Access the related garage's `name`
    )

@router.put("/{maintenance_id}", response_model=ResponseMaintenanceDTO)
def update_maintenance(
    maintenance_id: int,
    maintenance_update: UpdateMaintenanceDTO,  # Incoming update data
    db: Session = Depends(get_db)
):
    # Fetch the maintenance record
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()

    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")

    # Dynamically update the fields based on the incoming data
    for key, value in maintenance_update.dict(exclude_unset=True).items():
        setattr(maintenance, key, value)

    db.commit()  # Commit the changes
    db.refresh(maintenance)  # Refresh to get the updated record

    # Return the updated record in the response
    return ResponseMaintenanceDTO(
        id=maintenance.id,
        carId=maintenance.carId,
        garageId=maintenance.garageId,
        scheduledDate=maintenance.scheduledDate,
        serviceType=maintenance.serviceType,
        carName=maintenance.car.make,  # Assuming the `Car` model has a `make` field
        garageName=maintenance.garage.name  # Assuming the `Garage` model has a `name` field
    )

@router.delete("/{maintenance_id}")
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    db.delete(maintenance)
    db.commit()
    return {"detail": "Maintenance deleted successfully"}


# Helper function to get the number of days in a given month
def get_days_in_month(year: int, month: int) -> int:
    """Returns the number of days in a given month, considering leap years."""
    if month == 2:  # February
        return 29 if is_leap_year(year) else 28
    elif month in [4, 6, 9, 11]:  # April, June, September, November
        return 30
    else:  # January, March, May, July, August, October, December
        return 31


@router.get("/maintenance/monthlyRequestsReport", response_model=List[MonthlyRequestsReportDTO])
async def get_monthly_report(
        garageId: int = Query(..., description="The ID of the garage"),  # Accept as string
        startMonth: str = Query(..., description="Start month in 'YYYY-MM' format"),
        endMonth: str = Query(..., description="End month in 'YYYY-MM' format"),
        db: Session = Depends(get_db)
):
    # Convert garageId to an integer
    try:
        garage_id_int = int(garageId)  # Convert the string to an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid garageId format. It should be an integer.")

    # Parse the start and end months into integers for year and month
    try:
        start_year, start_month_num = map(int, startMonth.split("-"))
        end_year, end_month_num = map(int, endMonth.split("-"))
    except ValueError:
        raise HTTPException(status_code=400, detail="Start month and end month must be in 'YYYY-MM' format.")

    reports = []

    current_year = start_year
    current_month = start_month_num

    while (current_year < end_year) or (current_year == end_year and current_month <= end_month_num):
        month_value = get_month_value(current_year, current_month)
        leap_year = is_leap_year(current_year)

        year_month = YearMonth(
            year=current_year,
            month=current_month,
            leapYear=leap_year,
            monthValue=month_value
        )

        requests = get_request_count_for_month(db, garage_id_int, current_year, current_month)

        reports.append(MonthlyRequestsReportDTO(yearMonth=year_month, requests=requests))

        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1

    return reports
