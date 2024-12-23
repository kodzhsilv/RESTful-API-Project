from sqlalchemy import Column, Integer, String, ForeignKey, Table, ARRAY, JSON
from sqlalchemy.orm import relationship
from models.base import Base

car_garage_association = Table(
    "car_garage",
    Base.metadata,
    Column("car_id", Integer, ForeignKey("cars.id", ondelete="CASCADE"), primary_key=True),
    Column("garage_id", Integer, ForeignKey("garages.id", ondelete="CASCADE"), primary_key=True),
)
class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(255), index=True)
    model = Column(String(255), index=True)
    productionYear = Column(Integer)
    licensePlate = Column(String(255), unique=True, index=True)
    garageIds = Column(JSON, nullable=True)
    # Relationship to Garage model

    garages = relationship('Garage', secondary=car_garage_association, back_populates='cars')
    maintenances = relationship("Maintenance", back_populates="car")

def __repr__(self):
    return f"<Car(make={self.make}, model={self.model}, year={self.productionYear})>"
