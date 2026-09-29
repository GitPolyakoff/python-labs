import socket
import logging
from concurrent.futures import ThreadPoolExecutor
from protocol import JSONProtocol
from service import DeliveryService
from repository import DeliveryRepository
from exceptions import DeliveryNotFoundError, ProtocolError

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

class Server:
    def __init__(self, host: str, port: int, service: DeliveryService):
        self.host = host
        self.port = port
        self.service = service
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.executor = ThreadPoolExecutor(max_workers=10)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        logging.info(f"Сервер запущен на {self.host}:{self.port}")
        
        try:
            while True:
                conn, addr = self.server_socket.accept()
                logging.info(f"Client connected: {addr[0]}:{addr[1]}")
                self.executor.submit(self.handle_client, conn, addr)
        except KeyboardInterrupt:
            logging.info("Остановка сервера...")
        finally:
            self.server_socket.close()
            self.executor.shutdown()

    def handle_client(self, conn: socket.socket, addr: tuple):
        conn.settimeout(60)
        buffer = ""
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                buffer += data.decode('utf-8')
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        response_bytes = self.process_request(line.encode('utf-8'))
                        conn.sendall(response_bytes)
        except socket.timeout:
            logging.warning(f"Тайм-аут ожидания клиента {addr}")
        except Exception as e:
            logging.error(f"Ошибка при работе с клиентом {addr}: {e}")
        finally:
            logging.info(f"Client disconnected: {addr[0]}:{addr[1]}")
            conn.close()

    def process_request(self, raw_data: bytes) -> bytes:
        try:
            request = JSONProtocol.decode(raw_data)
            command = request.get("command")
            data = request.get("data", {})
            logging.info(f"Command: {command}")

            if command == "list":
                deliveries = [d.to_dict() for d in self.service.get_all_deliveries()]
                return JSONProtocol.encode_response("ok", data={"items": deliveries})
                
            elif command == "get":
                d_id = int(data["id"])
                delivery = self.service.get_delivery(d_id)
                return JSONProtocol.encode_response("ok", data=delivery.to_dict())
                
            elif command == "create":
                d = self.service.create_delivery(
                    int(data["id"]), data["address"], data["courier"], data["status"]
                )
                return JSONProtocol.encode_response("ok", data=d.to_dict())
                
            elif command == "update":
                d = self.service.update_delivery(
                    int(data["id"]), data["address"], data["courier"], data["status"]
                )
                return JSONProtocol.encode_response("ok", data=d.to_dict())
                
            elif command == "delete":
                self.service.delete_delivery(int(data["id"]))
                return JSONProtocol.encode_response("ok", data={})
                
            elif command == "get_by_status":
                status = data["status"]
                deliveries = [d.to_dict() for d in self.service.get_deliveries_by_status(status)]
                return JSONProtocol.encode_response("ok", data={"items": deliveries})
                
            else:
                return JSONProtocol.encode_response("error", error="Неизвестная команда")

        except DeliveryNotFoundError as e:
            return JSONProtocol.encode_response("error", error=str(e))
        except ProtocolError as e:
            return JSONProtocol.encode_response("error", error=str(e))
        except Exception as e:
            return JSONProtocol.encode_response("error", error="Внутренняя ошибка сервера")

if __name__ == "__main__":
    repo = DeliveryRepository()
    service = DeliveryService(repo)
    server = Server("127.0.0.1", 5000, service)
    server.start()