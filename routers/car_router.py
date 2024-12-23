from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from models.car import Car
from models.garage import Garage
from schemas.car import ResponseCarDTO, CreateCarDTO, UpdateCarDTO
from services.car_service import CarService
from repositories.car_repository import CarRepository
from config.db import get_db, get_db_session

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.get("", response_model=list[ResponseCarDTO])
async def list_cars(
    carMake: Optional[str] = None,
    garageId: Optional[int] = None,
    db: Session = Depends(get_db_session),
):
    """
    List cars with optional filters by car make or garage ID.
    """
    # Base query for cars
    query = db.query(Car)

    # Apply filters
    if carMake:
        query = query.filter(Car.make.ilike(f"%{carMake}%"))
    if garageId:
        query = query.filter(Car.garageIds.any(garageId))  # Assuming garageIds is a list

    cars = query.all()

    # Fetch all garages and map them by ID
    all_garages = db.query(Garage).all()
    garage_map = {
        garage.id: {
            "name": garage.name,
            "location": garage.location,
            "city": garage.city,
            "capacity": garage.capacity
        }
        for garage in all_garages
    }

    # Prepare the response
    response = []
    for car in cars:
        garages = [
            {
                "id": garage_id,
                "name": garage_map[garage_id]["name"],
                "location": garage_map[garage_id]["location"],
                "city": garage_map[garage_id]["city"],
                "capacity": garage_map[garage_id]["capacity"]
            }
            for garage_id in car.garageIds if garage_id in garage_map
        ]
        response.append(
            {
                "id": car.id,
                "make": car.make,
                "model": car.model,
                "productionYear": car.productionYear,
                "licensePlate": car.licensePlate,
                "garageIds": car.garageIds,
                "garages": garages,
            }
        )

    return response
#def list_cars(db: Session = Depends(get_db)):
#    service = CarService(CarRepository(db))
#    return service.list_cars()


@router.get("/{car_id}", response_model=ResponseCarDTO)
#def get_car(car_id: int, db: Session = Depends(get_db)):
 #   service = CarService(CarRepository(db))
  #  car = service.get_car(car_id)
   # if not car:
    #    raise HTTPException(status_code=404, detail="Car not found")
    #return car
async def get_car(car_id: int, db: Session = Depends(get_db_session)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return {
        "id": car.id,
        "make": car.make,
        "model": car.model,
        "productionYear": car.productionYear,
        "licensePlate": car.licensePlate,
        "garageIds": [garage.id for garage in car.garages],  # Return garage IDs
    }

#@router.post("", response_model=ResponseCarDTO)
#def create_car(car: CreateCarDTO, db: Session = Depends(get_db)):
 #   service = CarService(CarRepository(db))
  #  return service.create_car(car.dict())#
@router.post("", response_model=ResponseCarDTO)
async def create_car(car: CreateCarDTO, db: Session = Depends(get_db)):
    new_car = Car(
        make=car.make,
        model=car.model,
        productionYear=car.productionYear,
        licensePlate=car.licensePlate,
        garageIds=car.garageIds  # Store the array of garage IDs
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car
@router.put("/{car_id}", response_model=ResponseCarDTO)
def update_car(car_id: int, car_update: UpdateCarDTO, db: Session = Depends(get_db)):
    service = CarService(CarRepository(db))
    updated_car = service.update_car(car_id, car_update)
    if not updated_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated_car

@router.delete("/{car_id}", response_model=ResponseCarDTO)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    service = CarService(CarRepository(db))
    deleted_car = service.delete_car(car_id)
    if not deleted_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return deleted_car