from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.car import car_garage_association


class Garage(Base):
    __tablename__ = "garages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    location = Column(String(255))
    city = Column(String(255))
    capacity = Column(Integer)
    # Relationship to the Car table
    maintenances = relationship("Maintenance", back_populates="garage")
    cars = relationship('Car', secondary=car_garage_association, back_populates='garages')
    def __repr__(self):
        return f"<Garage(name={self.name}, location={self.location}, city={self.city}, capacity={self.capacity})>"
