from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Garage(Base):
    __tablename__ = "garages"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    city = Column(String)
    capacity = Column(Integer)

    # Relationship to the Car table
    cars = relationship("Car", back_populates="garage")
    maintenances = relationship("Maintenance", back_populates="garage")

    def __repr__(self):
        return f"<Garage(name={self.name}, location={self.location}, city={self.city}, capacity={self.capacity})>"
