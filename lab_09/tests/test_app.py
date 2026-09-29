import unittest
from models import Delivery
from repository import DeliveryRepository
from service import DeliveryService
from exceptions import DeliveryNotFoundError
from protocol import JSONProtocol

class TestApp(unittest.TestCase):
    def setUp(self):
        self.repo = DeliveryRepository()
        self.service = DeliveryService(self.repo)

    def test_repository_add_and_get(self):
        d = Delivery(1, "ул. Мира 10", "Иван", "создана")
        self.repo.add(d)
        retrieved = self.repo.get(1)
        self.assertEqual(retrieved.address, "ул. Мира 10")

    def test_repository_delete_not_found(self):
        with self.assertRaises(DeliveryNotFoundError):
            self.repo.delete(999)

    def test_service_create_delivery(self):
        d = self.service.create_delivery(2, "ул. Ленина 5", "Анна", "в пути")
        self.assertEqual(len(self.service.get_all_deliveries()), 1)
        self.assertEqual(d.courier_name, "Анна")

    def test_service_get_by_status(self):
        self.service.create_delivery(1, "А", "К", "в пути")
        self.service.create_delivery(2, "Б", "К", "доставлена")
        self.service.create_delivery(3, "В", "К", "в пути")
        
        in_transit = self.service.get_deliveries_by_status("в пути")
        self.assertEqual(len(in_transit), 2)

    def test_protocol_encode_decode(self):
        command = "get"
        data = {"id": 5}
        encoded = JSONProtocol.encode_request(command, data)
        
        decoded = JSONProtocol.decode(encoded)
        self.assertEqual(decoded["command"], "get")
        self.assertEqual(decoded["data"]["id"], 5)

if __name__ == "__main__":
    unittest.main()