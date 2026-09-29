from repository import DeliveryRepository
from models import Delivery

class DeliveryService:
    def __init__(self, repository: DeliveryRepository):
        self.repo = repository

    def create_delivery(self, d_id: int, address: str, courier: str, status: str) -> Delivery:
        delivery = Delivery(d_id, address, courier, status)
        self.repo.add(delivery)
        return delivery

    def get_delivery(self, d_id: int) -> Delivery:
        return self.repo.get(d_id)

    def get_all_deliveries(self) -> list[Delivery]:
        return self.repo.get_all()

    def update_delivery(self, d_id: int, address: str, courier: str, status: str) -> Delivery:
        self.repo.get(d_id)
        updated = Delivery(d_id, address, courier, status)
        self.repo.update(updated)
        return updated

    def delete_delivery(self, d_id: int) -> None:
        self.repo.delete(d_id)

    def get_deliveries_by_status(self, status: str) -> list[Delivery]:
        all_deliveries = self.repo.get_all()
        return [d for d in all_deliveries if d.status.lower() == status.lower()]