from repositories.maintenance_repository import MaintenanceRepository
from typing import Optional, List
from models.maintenance import Maintenance
from sqlalchemy.orm import Session
from schemas.maintenance import MonthlyRequestReportDTO
from datetime import date
from repositories.maintenance_repository import MaintenanceRepository


class MaintenanceService:
    def __init__(self, repository: MaintenanceRepository):
        self.repository = repository

    def list_maintenances(self) -> List[Maintenance]:
        return self.repository.list_maintenances()

    def get_maintenance(self, maintenance_id: int) -> Optional[Maintenance]:
        return self.repository.get_maintenance(maintenance_id)

    def create_maintenance(self, maintenance_data: dict) -> Maintenance:
        # You can add any additional business logic here, such as validating service types or checking scheduled dates
        return self.repository.create_maintenance(maintenance_data)

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
        MonthlyRequestReportDTO]:
        # Call the repository to fetch the data
        monthly_data = self.repository.get_monthly_request_report(garage_id, start_month, end_month)

        # Convert the data into MonthlyRequestReportDTO
        return [
            MonthlyRequestReportDTO(yearMonth=month, requests=requests)
            for month, requests in monthly_data
        ]