from sqlalchemy.orm import Session
from schemas.car import CreateCarDTO, UpdateCarDTO
from models.car import Car

class CarRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_cars(self):
        return self.db.query(Car).all()

    def get_car(self, car_id: int):
        return self.db.query(Car).filter(Car.id == car_id).first()

    def create_car(self, car_data: dict) -> Car:
        new_car = Car(**car_data)
        self.db.add(new_car)
        self.db.commit()
        self.db.refresh(new_car)
        return new_car

    def get_by_id(self, car_id: int):
        return self.db.query(Car).filter(Car.id == car_id).first()

    def update_car(self, car_id: int, car_data: UpdateCarDTO):
        car = self.get_by_id(car_id)
        if not car:
            raise ValueError(f"Car with ID {car_id} does not exist.")
        car_data_dict = car_data.dict(exclude_unset=True)
        for key, value in car_data_dict.items():
            setattr(car, key, value)
        self.db.commit()
        self.db.refresh(car)
        return car

    def delete_car(self, car_id: int):
        car = self.get_car(car_id)
        if not car:
            return None
        self.db.delete(car)
        self.db.commit()
        return car
