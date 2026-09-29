import json
from exceptions import ProtocolError

class JSONProtocol:
    @staticmethod
    def encode_request(command: str, data: dict) -> bytes:
        message = {"command": command, "data": data}
        return (json.dumps(message) + "\n").encode('utf-8')

    @staticmethod
    def encode_response(status: str, data: dict = None, error: str = None) -> bytes:
        message = {"status": status}
        if data is not None:
            message["data"] = data
        if error is not None:
            message["error"] = error
        return (json.dumps(message) + "\n").encode('utf-8')

    @staticmethod
    def decode(raw_data: bytes) -> dict:
        try:
            text = raw_data.decode('utf-8').strip()
            if not text:
                raise ProtocolError("Пустое сообщение")
            return json.loads(text)
        except json.JSONDecodeError:
            raise ProtocolError("Некорректный JSON")