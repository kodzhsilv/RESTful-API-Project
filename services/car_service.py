from repositories.car_repository import CarRepository

class CarService:
    def __init__(self, repository: CarRepository):
        self.repository = repository

    def list_cars(self):
        return self.repository.list_cars()

    def get_car(self, car_id: int):
        return self.repository.get_car(car_id)

    def create_car(self, car_data: dict):
        # Add any business logic here before saving the car
        return self.repository.create_car(car_data)

    def update_car(self, car_id: int, car_data: dict):
        return self.repository.update_car(car_id, car_data)

    def delete_car(self, car_id: int):
        return self.repository.delete_car(car_id)
