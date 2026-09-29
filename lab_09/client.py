import socket
from protocol import JSONProtocol

class DeliveryClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(10)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Подключено к серверу {self.host}:{self.port}")
        except ConnectionRefusedError:
            print("Ошибка: Сервер недоступен.")
            exit(1)

    def send_command(self, command: str, data: dict):
        try:
            req_bytes = JSONProtocol.encode_request(command, data)
            self.client_socket.sendall(req_bytes)
            
            buffer = ""
            while True:
                chunk = self.client_socket.recv(1024).decode('utf-8')
                if not chunk:
                    print("Соединение разорвано сервером.")
                    break
                buffer += chunk
                if '\n' in buffer:
                    line = buffer.split('\n')[0]
                    response = JSONProtocol.decode(line.encode('utf-8'))
                    self.print_response(response)
                    break
        except socket.timeout:
            print("Ошибка: Превышено время ожидания ответа от сервера (тайм-аут).")
        except Exception as e:
            print(f"Сетевая ошибка: {e}")

    def print_response(self, response: dict):
        if response.get("status") == "ok":
            print("\nУСПЕХ!")
            if "data" in response and response["data"]:
                print("Данные:", response["data"])
        else:
            print(f"\nОШИБКА: {response.get('error')}")

    def run(self):
        self.connect()
        while True:
            print("\n=== МЕНЮ КЛИЕНТА (Курьерская служба) ===")
            print("1. Получить список всех доставок")
            print("2. Получить доставку по ID")
            print("3. Создать доставку")
            print("4. Изменить доставку")
            print("5. Удалить доставку")
            print("6. Получить доставки по статусу (Спец. операция)")
            print("0. Выход")
            
            choice = input("Введите команду: ")
            
            if choice == "1":
                self.send_command("list", {})
            elif choice == "2":
                d_id = int(input("Введите ID доставки: "))
                self.send_command("get", {"id": d_id})
            elif choice == "3":
                d_id = int(input("ID: "))
                address = input("Адрес: ")
                courier = input("Курьер: ")
                status = input("Статус: ")
                self.send_command("create", {"id": d_id, "address": address, "courier": courier, "status": status})
            elif choice == "4":
                d_id = int(input("ID существующей доставки: "))
                address = input("Новый адрес: ")
                courier = input("Новый курьер: ")
                status = input("Новый статус: ")
                self.send_command("update", {"id": d_id, "address": address, "courier": courier, "status": status})
            elif choice == "5":
                d_id = int(input("Введите ID для удаления: "))
                self.send_command("delete", {"id": d_id})
            elif choice == "6":
                status = input("Введите искомый статус (например, 'в пути'): ")
                self.send_command("get_by_status", {"status": status})
            elif choice == "0":
                print("Отключение...")
                self.client_socket.close()
                break
            else:
                print("Неизвестная команда.")

if __name__ == "__main__":
    client = DeliveryClient("127.0.0.1", 5000)
    client.run()