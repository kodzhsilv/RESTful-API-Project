from sqlalchemy.orm import Session
from models.maintenance import Maintenance
from datetime import datetime
from datetime import date
from typing import List

class MaintenanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_maintenances(self):
        return self.db.query(Maintenance).all()

    def get_maintenance(self, maintenance_id: int):
        return self.db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()

    def create_maintenance(self, maintenance_data: dict):
        new_maintenance = Maintenance(**maintenance_data)
        self.db.add(new_maintenance)
        self.db.commit()
        self.db.refresh(new_maintenance)
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

    def get_monthly_request_report(self, garage_id: int, start_month: str, end_month: str, db: Session ):
        # Convert the start and end months to datetime objects
        start_date = datetime.strptime(start_month + '-01', "%Y-%m-%d")
        end_date = datetime.strptime(end_month + '-01', "%Y-%m-%d")

        # Query the database for the number of requests for each month in the range
        query = db.query(Maintenance.scheduled_date).filter(
            Maintenance.garage_id == garage_id,
            Maintenance.scheduled_date >= start_date,
            Maintenance.scheduled_date <= end_date
        ).all()

        # Process the query results to count the requests per month
        monthly_data = {}
        for maintenance in query:
            year_month = maintenance.date.strftime('%Y-%m')
            if year_month not in monthly_data:
                monthly_data[year_month] = 0
            monthly_data[year_month] += 1

        # Convert the dictionary into a sorted list of tuples
        return sorted(monthly_data.items())

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