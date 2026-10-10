from contextlib import contextmanager

@contextmanager
def transaction_context(account_id: int):
    print(f"\n[ТРАНЗАКЦИЯ] Начало операции для счёта {account_id}")
    try:
        yield
        print("[ТРАНЗАКЦИЯ] Операция успешно завершена")
    except Exception as e:
        print(f"[ТРАНЗАКЦИЯ] Ошибка во время операции: {e}")
        raise