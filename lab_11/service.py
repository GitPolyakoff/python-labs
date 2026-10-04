import redis
import uuid
from repository import AccountRepository

class BankService:
    def __init__(self):
        self.repo = AccountRepository()
        # подключаюсь к redis для хранения сессий
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True, protocol=2)
            self.redis_client.ping()
            self.redis_active = True
        except redis.ConnectionError:
            print("ВНИМАНИЕ: Redis сервер не запущен. Сессии работать не будут.")
            self.redis_active = False

    def get_all_accounts(self):
        return self.repo.get_all()

    def get_account(self, acc_id: int):
        return self.repo.get_by_id(acc_id)

    def process_transfer(self, from_id: int, to_id: int, amount: float):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.repo.transfer_money(from_id, to_id, amount)

    #работа с сессиями
    def login_user(self, client_id: int):
        if not self.redis_active:
            raise RuntimeError("Redis недоступен")
        
        session_token = str(uuid.uuid4())
        # сохраняю сессию в redis
        self.redis_client.setex(f"session:{session_token}", 60, str(client_id))
        return session_token

    def check_session(self, token: str):
        if not self.redis_active:
            raise RuntimeError("Redis недоступен")
            
        client_id = self.redis_client.get(f"session:{token}")
        if not client_id:
            raise ValueError("Сессия истекла или не существует")
        return int(client_id)