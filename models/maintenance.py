from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Maintenance(Base):
    __tablename__ = "maintenances"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"))  # Foreign key to Car model
    garage_id = Column(Integer, ForeignKey("garages.id"))  # Foreign key to Garage model
    service_type = Column(String)
    scheduled_date = Column(Date)


    # Relationships
    car = relationship("Car", back_populates="maintenances")
    garage = relationship("Garage", back_populates="maintenances")

    def __repr__(self):
        return f"<Maintenance(service_type={self.service_type}, scheduled_date={self.scheduled_date}, car_id={self.car_id}, garage_id={self.garage_id})>"
