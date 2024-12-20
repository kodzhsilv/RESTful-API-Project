from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.car import ResponseCarDTO, CreateCarDTO, UpdateCarDTO
from services.car_service import CarService
from repositories.car_repository import CarRepository
from config.db import get_db

router = APIRouter(prefix="/api/cars", tags=["Cars"])

@router.get("/", response_model=list[ResponseCarDTO])
def list_cars(db: Session = Depends(get_db)):
    service = CarService(CarRepository(db))
    return service.list_cars()

@router.get("/{car_id}", response_model=ResponseCarDTO)
def get_car(car_id: int, db: Session = Depends(get_db)):
    service = CarService(CarRepository(db))
    car = service.get_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.post("/", response_model=ResponseCarDTO)
def create_car(car: CreateCarDTO, db: Session = Depends(get_db)):
    service = CarService(CarRepository(db))
    return service.create_car(car.dict())

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