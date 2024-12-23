from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from schemas.garage import CreateGarageDTO, ResponseGarageDTO, UpdateGarageDTO
from schemas.garage import GarageDailyAvailabilityRequestDTO, GarageDailyAvailabilityReportDTO
from services.garage_service import GarageService
from repositories.garage_repository import GarageRepository
from config.db import get_db
from models.garage import Garage
from pydantic import BaseModel

router = APIRouter(prefix="/garages", tags=["Garages"])
@router.get("", response_model=List[ResponseGarageDTO])
def list_garages(city: str = None, db: Session = Depends(get_db)):
    # Pass city filter to the service
    service = GarageService(GarageRepository(db))
    return service.list_garages(city)
# List all garages
#@router.get("", response_model=list[ResponseGarageDTO])
#def list_garages(db: Session = Depends(get_db)):
#    service = GarageService(GarageRepository(db))
#    return service.list_garages()
#
# Get a specific garage by ID
@router.get("/{garage_id}", response_model=ResponseGarageDTO)
def get_garage(garage_id: int, db: Session = Depends(get_db)):
    service = GarageService(GarageRepository(db))
    garage = service.get_garage(garage_id)
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return garage

# Create a new garage
@router.post("", response_model=ResponseGarageDTO)
def create_garage(garage: CreateGarageDTO, db: Session = Depends(get_db)):
    service = GarageService(GarageRepository(db))
    return service.create_garage(garage.dict())

# Update an existing garage
@router.put("/{garage_id}", response_model=ResponseGarageDTO)
def update_garage(garage_id: int, garage: CreateGarageDTO, db: Session = Depends(get_db)):
    service = GarageService(GarageRepository(db))
    updated_garage = service.update_garage(garage_id, garage.dict())
    if not updated_garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return updated_garage

# Delete a garage
@router.delete("/{garage_id}", response_model=ResponseGarageDTO)
def delete_garage(garage_id: int, db: Session = Depends(get_db)):
    service = GarageService(GarageRepository(db))
    deleted_garage = service.delete_garage(garage_id)
    if not deleted_garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return deleted_garage

@router.post("/garage-availability", response_model=list[GarageDailyAvailabilityReportDTO])
def get_daily_availability_report(
    request: GarageDailyAvailabilityRequestDTO,
    db: Session = Depends(get_db)
):
    service = GarageService(GarageRepository(db))
    reports = service.get_garage_daily_availability(
        request.garageId, request.startDate, request.endDate, db
    )
    return reports
@router.put("/{garage_id}", response_model=ResponseGarageDTO)
def update_garage(
    garage_id: int,
    garage: UpdateGarageDTO,
    db: Session = Depends(get_db)
):
    service = GarageService(GarageRepository(db))
    updated_garage = service.update_garage(garage_id, garage)
    if not updated_garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return updated_garage
