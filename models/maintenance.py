from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Maintenance(Base):
    __tablename__ = "maintenances"

    id = Column(Integer, primary_key=True, index=True)
    carId = Column(Integer, ForeignKey("cars.id"))  # Foreign key to Car model
    garageId = Column(Integer, ForeignKey("garages.id"))  # Foreign key to Garage model
    serviceType = Column(String(255))
    scheduledDate = Column(Date)


    # Relationships
    car = relationship("Car", back_populates="maintenances")
    garage = relationship("Garage", back_populates="maintenances")

    def __repr__(self):
        return f"<Maintenance(service_type={self.serviceType}, scheduled_date={self.scheduledDate}, car_id={self.carId}, garage_id={self.garageId})>"
