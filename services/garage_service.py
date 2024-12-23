from typing import Optional, List

from models.garage import Garage
from repositories.garage_repository import GarageRepository
from schemas.garage import UpdateGarageDTO, ResponseGarageDTO
from sqlalchemy.orm import Session
from datetime import date

class GarageService:
    def __init__(self, repository: GarageRepository):
        self.repository = repository

    def list_garages(self, city: str = None) -> List[Garage]:
        # Call the repository method to filter by city if provided
        return self.repository.list_garages(city)
  # def list_garages(self):
  #     return self.repository.list_garages()

    def get_garage(self, garage_id: int):
        return self.repository.get_garage(garage_id)

    def create_garage(self, garage_data: dict):
        # Add any business logic or validations here if needed
        return self.repository.create_garage(garage_data)

    def update_garage(self, garage_id: int, garage_data: dict):
        # Check if the garage exists before updating
        existing_garage = self.repository.get_garage(garage_id)
        if not existing_garage:
            return None
        return self.repository.update_garage(garage_id, garage_data)

    def delete_garage(self, garage_id: int):
        # Check if the garage exists before deleting
        existing_garage = self.repository.get_garage(garage_id)
        if not existing_garage:
            return None
        return self.repository.delete_garage(garage_id)

    def get_garage_daily_availability(self, garage_id: int, start_date: date, end_date: date, db: Session):
        return self.repository.get_availability_report(garage_id, start_date, end_date)
