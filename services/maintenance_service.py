from sqlalchemy import func

from models.car import Car
from models.garage import Garage
from repositories.maintenance_repository import MaintenanceRepository
from typing import Optional, List
from sqlalchemy.orm import Session
from models.maintenance import Maintenance
from sqlalchemy.orm import Session
from schemas.maintenance import MonthlyRequestsReportDTO, CreateMaintenanceDTO, ResponseMaintenanceDTO
from datetime import date, datetime
from repositories.maintenance_repository import MaintenanceRepository


class MaintenanceService:
    def __init__(self, repository: MaintenanceRepository):
        self.repository = repository

    def list_maintenances(self) -> List[Maintenance]:
        return self.repository.list_maintenances()

    #def get_maintenance(self, maintenance_id: int) -> Optional[Maintenance]:
    #    return self.repository.get_maintenance(maintenance_id)

    def get_maintenance(self) -> List[ResponseMaintenanceDTO]:
        # Get all maintenance records with related car and garage
        maintenance_records = self.repository.query(Maintenance).join(Car).join(Garage).all()

        # Map the results to the ResponseMaintenanceDTO
        return [
            ResponseMaintenanceDTO(
                id=maintenance.id,
                carId=maintenance.carId,
                carName=maintenance.car.name,  # Assuming the `Car` model has a `name` field
                garageId=maintenance.garageId,
                garageName=maintenance.garage.name,  # Assuming the `Garage` model has a `name` field
                scheduledDate=maintenance.scheduledDate,
                serviceType=maintenance.serviceType
            ) for maintenance in maintenance_records
        ]
    def create_maintenance(self, maintenance_data: CreateMaintenanceDTO):
        # Directly pass the Pydantic model to the repository
        new_maintenance = self.repository.create_maintenance(maintenance_data)

        return {
            "car_id": new_maintenance.car_id,
            "garage_id": new_maintenance.garage_id,
            "service_type": new_maintenance.service_type,
            "scheduled_date": new_maintenance.scheduled_date
        }
   #def create_maintenance(self, maintenance_data: dict) -> Maintenance:
   #    # You can add any additional business logic here, such as validating service types or checking scheduled dates
   #    return self.repository.create_maintenance(maintenance_data)

    def update_maintenance(self, maintenance_id: int, maintenance_data: dict) -> Optional[Maintenance]:
        # Check if the maintenance exists before updating
        existing_maintenance = self.repository.get_maintenance(maintenance_id)
        if not existing_maintenance:
            return None
        return self.repository.update_maintenance(maintenance_id, maintenance_data)

    def delete_maintenance(self, maintenance_id: int) -> Optional[Maintenance]:
        # Check if the maintenance exists before deleting
        existing_maintenance = self.repository.get_maintenance(maintenance_id)
        if not existing_maintenance:
            return None
        return self.repository.delete_maintenance(maintenance_id)

    def get_monthly_request_report(self, garage_id: int, start_month: str, end_month: str) -> List[
        MonthlyRequestsReportDTO]:
        # Call the repository to fetch the data
        monthly_data = self.repository.get_monthly_request_report(garage_id, start_month, end_month)

        # Convert the data into MonthlyRequestReportDTO
        return [
            MonthlyRequestsReportDTO(yearMonth=month, requests=requests)
            for month, requests in monthly_data
        ]

def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_month_value(year: int, month: int) -> int:
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if month == 2 and is_leap_year(year):
            return 29  # February in a leap year
        return month_days[month - 1]


def get_request_count_for_month(db: Session, garage_id: int, year: int, month: int) -> int:
    return db.query(Maintenance).filter(
        Maintenance.garageId == garage_id,
        Maintenance.scheduledDate >= datetime(year, month, 1),
        Maintenance.scheduledDate < datetime(year, month + 1, 1)
    ).count()
