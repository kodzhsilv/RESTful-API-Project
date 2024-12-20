from sqlalchemy.orm import Session
from models.car import Car

class CarRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_cars(self):
        return self.db.query(Car).all()

    def get_car(self, car_id: int):
        return self.db.query(Car).filter(Car.id == car_id).first()

    def create_car(self, car_data: dict):
        new_car = Car(**car_data)
        self.db.add(new_car)
        self.db.commit()
        self.db.refresh(new_car)
        return new_car

    def update_car(self, car_id: int, car_data: dict):
        car = self.get_car(car_id)
        if not car:
            return None
        for key, value in car_data.items():
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
