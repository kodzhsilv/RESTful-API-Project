from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models.garage import Garage
from datetime import date, timedelta
from models.maintenance import Maintenance
from fastapi import HTTPException
from schemas.garage import UpdateGarageDTO

class GarageRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_garages(self):
        return self.db.query(Garage).all()

    def get_garage(self, garage_id: int):
        return self.db.query(Garage).filter(Garage.id == garage_id).first()

    def create_garage(self, garage_data: dict):
        new_garage = Garage(**garage_data)
        self.db.add(new_garage)
        self.db.commit()
        self.db.refresh(new_garage)
        return new_garage

    def update_garage(self, garage_id: int, garage_data: dict):
        garage = self.get_garage(garage_id)
        if not garage:
            return None
        for key, value in garage_data.items():
            setattr(garage, key, value)
        self.db.commit()
        self.db.refresh(garage)
        return garage

    def delete_garage(self, garage_id: int):
        garage = self.get_garage(garage_id)
        if not garage:
            return None
        self.db.delete(garage)
        self.db.commit()
        return garage

    def get_availability_report(garage_id: int, start_date: date, end_date: date, db: Session):
        # Step 1: Validate Garage existence
        garage = db.query(Garage).filter(Garage.id == garage_id).first()
        if not garage:
            raise HTTPException(status_code=404, detail="Garage not found")

        capacity = garage.capacity

        # Step 2: Query maintenance data
        maintenance_query = (
            db.query(
                Maintenance.scheduled_date.label("date"),
                func.count(Maintenance.id).label("requests")
            )
            .filter(
                Maintenance.garage_id == garage_id,
                Maintenance.scheduled_date >= start_date,
                Maintenance.scheduled_date <= end_date
            )
            .group_by(Maintenance.scheduled_date)
            .all()
        )

        # Step 3: Map requests by date
        requests_by_date = {record.date: record.requests for record in maintenance_query}

        # Step 4: Generate the availability report
        report = []
        current_date = start_date
        while current_date <= end_date:
            requests = requests_by_date.get(current_date, 0)  # Default to 0 if no requests
            available_capacity = max(0, capacity - requests)  # Ensure no negative capacity

            report.append({
                "date": current_date,
                "requests": requests,
                "availableCapacity": available_capacity
            })
            current_date += timedelta(days=1)

        return report