from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Car(Base):
    __tablename__ = "cars"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    productionYear = Column(Integer)
    license_plate = Column(String, unique=True, index=True)
    garages = Column(Integer, ForeignKey("garages.id"))

    # Relationship to the Garage table
    garage = relationship("Garage", back_populates="cars")
    maintenances = relationship("Maintenance", back_populates="car")

    def __repr__(self):
        return f"<Car(make={self.make}, model={self.model}, year={self.productionYear})>"
