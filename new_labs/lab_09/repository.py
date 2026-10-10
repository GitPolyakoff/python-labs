from models import Delivery
from exceptions import DeliveryNotFoundError

class DeliveryRepository:
    def __init__(self):
        self._storage: dict[int, Delivery] = {}

    def add(self, delivery: Delivery) -> None:
        self._storage[delivery.id] = delivery

    def get(self, delivery_id: int) -> Delivery:
        if delivery_id not in self._storage:
            raise DeliveryNotFoundError(f"Доставка с ID {delivery_id} не найдена.")
        return self._storage[delivery_id]

    def get_all(self) -> list[Delivery]:
        return list(self._storage.values())

    def update(self, delivery: Delivery) -> None:
        if delivery.id not in self._storage:
            raise DeliveryNotFoundError("Нельзя обновить несуществующую доставку.")
        self._storage[delivery.id] = delivery

    def delete(self, delivery_id: int) -> None:
        if delivery_id not in self._storage:
            raise DeliveryNotFoundError("Нельзя удалить несуществующую доставку.")
        del self._storage[delivery_id]