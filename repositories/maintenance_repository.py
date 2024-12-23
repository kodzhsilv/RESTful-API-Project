from sqlalchemy import func
from sqlalchemy.orm import Session
from models.maintenance import Maintenance
from datetime import datetime
from datetime import date
from typing import List, Tuple, Dict

from schemas.maintenance import CreateMaintenanceDTO


class MaintenanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_maintenances(self):
        return self.db.query(Maintenance).all()

    def get_maintenance(self, maintenance_id: int):
        return self.db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()

    def create_maintenance(self, maintenance_data: CreateMaintenanceDTO):
        # Convert the Pydantic model directly to the database model
        new_maintenance = Maintenance(
            car_id=maintenance_data.car_id,
            garage_id=maintenance_data.garage_id,
            service_type=maintenance_data.service_type,
            scheduled_date=maintenance_data.scheduled_date
        )

        # Add the new maintenance record to the session
        self.db.add(new_maintenance)
        self.db.commit()

        return new_maintenance

    def update_maintenance(self, maintenance_id: int, maintenance_data: dict):
        maintenance = self.get_maintenance(maintenance_id)
        if not maintenance:
            return None
        for key, value in maintenance_data.items():
            setattr(maintenance, key, value)
        self.db.commit()
        self.db.refresh(maintenance)
        return maintenance

    def delete_maintenance(self, maintenance_id: int):
        maintenance = self.get_maintenance(maintenance_id)
        if not maintenance:
            return None
        self.db.delete(maintenance)
        self.db.commit()
        return maintenance

    def list_maintenance(self, car_id: int, garage_id: int, start_date: date, end_date: date) -> List[Maintenance]:
        query = self.db.query(Maintenance)
        if car_id:
            query = query.filter(Maintenance.car_id == car_id)
        if garage_id:
            query = query.filter(Maintenance.garage_id == garage_id)
        if start_date:
            query = query.filter(Maintenance.scheduled_date >= start_date)
        if end_date:
            query = query.filter(Maintenance.scheduled_date <= end_date)
        return query.all()

    def get_monthly_request_report(self, garage_id: int, start_month: str, end_month: str) -> List[Tuple[str, int]]:
        start_date = datetime.strptime(start_month, "%Y-%m")
        end_date = datetime.strptime(end_month, "%Y-%m")
        query = (
            self.db.query(
                func.date_trunc('month', Maintenance.scheduled_date).label('yearMonth'),
                func.count(Maintenance.id).label('requests')
            )
            .filter(Maintenance.garage_id == garage_id)
            .filter(Maintenance.scheduled_date >= start_date)
            .filter(Maintenance.scheduled_date <= end_date)
            .group_by(func.date_trunc('month', Maintenance.scheduled_date))
            .order_by(func.date_trunc('month', Maintenance.scheduled_date))
            .all()
        )
        return query
