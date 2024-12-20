from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.maintenance import CreateMaintenanceDTO, ResponseMaintenanceDTO
from schemas.maintenance import MonthlyRequestReportDTO
from services.maintenance_service import MaintenanceService
from repositories.maintenance_repository import MaintenanceRepository
from config.db import get_db
from typing import List  # Add this import
from typing import Optional
from fastapi import Query
from datetime import date
from schemas.maintenance import ResponseMaintenanceDTO

router = APIRouter(prefix="/api/maintenance", tags=["Maintenances"])

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

@router.get("/monthlyRequestsReport", response_model=List[MonthlyRequestReportDTO])
async def get_monthly_request_report_route(
    garage_id: int = Query(..., description="The ID of the garage"),
    start_month: str = Query(..., description="Start month in 'YYYY-MM' format"),
    end_month: str = Query(..., description="End month in 'YYYY-MM' format"),
    db: Session = Depends(get_db)  # Dependency for database session
):
    # Instantiate the service and get the monthly report
    service = MaintenanceService(db)
    return service.get_monthly_request_report(garage_id, start_month, end_month)