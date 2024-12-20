from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.maintenance import CreateMaintenanceDTO, ResponseMaintenanceDTO
from schemas.maintenance import MonthlyRequestReportDTO, MonthlyRequestReportRequestDTO
from services.maintenance_service import MaintenanceService
from repositories.maintenance_repository import MaintenanceRepository
from config.db import get_db
from typing import List  # Add this import
from typing import Optional
from fastapi import Query
from datetime import date
from schemas.maintenance import ResponseMaintenanceDTO

router = APIRouter(prefix="/api/maintenance", tags=["Maintenances"])


@router.get("/", response_model=List[ResponseMaintenanceDTO])
def list_maintenance( carId: int = Query(None, description="Filter by car ID"),
    garageId: int = Query(None, description="Filter by garage ID"),
    startDate: date = Query(None, description="Filter by start date"),
    endDate: date = Query(None, description="Filter by end date"),
    db: Session = Depends(get_db)):
    """
    Retrieve a list of maintenance records, optionally filtered by car ID, garage ID,
    and date range.
    """
    service = MaintenanceService(MaintenanceRepository(db))
    try:
        maintenances = service.get_maintenance_records(
            car_id=carId,
            garage_id=garageId,
            start_date=startDate,
            end_date=endDate,
        )
        return maintenances
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a specific maintenance by ID
@router.get("/{maintenance_id}", response_model=ResponseMaintenanceDTO)
def get_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    service = MaintenanceService(MaintenanceRepository(db))
    maintenance = service.get_maintenance(maintenance_id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return maintenance

# Create a new maintenance record
@router.post("/", response_model=ResponseMaintenanceDTO)
def create_maintenance(maintenance: CreateMaintenanceDTO, db: Session = Depends(get_db)):
    service = MaintenanceService(MaintenanceRepository(db))
    return service.create_maintenance(maintenance.dict())

# Update an existing maintenance record
@router.put("/{maintenance_id}", response_model=ResponseMaintenanceDTO)
def update_maintenance(maintenance_id: int, maintenance: CreateMaintenanceDTO, db: Session = Depends(get_db)):
    service = MaintenanceService(MaintenanceRepository(db))
    updated_maintenance = service.update_maintenance(maintenance_id, maintenance.dict())
    if not updated_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return updated_maintenance

# Delete a maintenance record
@router.delete("/{maintenance_id}", response_model=ResponseMaintenanceDTO)
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    service = MaintenanceService(MaintenanceRepository(db))
    deleted_maintenance = service.delete_maintenance(maintenance_id)
    if not deleted_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return deleted_maintenance

@router.post("/monthly-requests-report", response_model=list[MonthlyRequestReportDTO])
def get_monthly_request_report(
    report_request: MonthlyRequestReportRequestDTO, db: Session = Depends(get_db)
):
    service = MaintenanceService(MaintenanceRepository(db))
    report = service.get_monthly_request_report(
        report_request.garageId, report_request.startMonth, report_request.endMonth, db
    )
    return report