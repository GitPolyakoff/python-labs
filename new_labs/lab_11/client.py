import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def print_response(response):
    print(f"\n--- HTTP {response.status_code} ---")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
        print("Заголовки:", response.headers)

def run():
    current_token = None
    
    while True:
        print("\n=========================")
        print("1. Получить все счета (из SQLite JOIN)")
        print("2. Перевод средств (Транзакция SQLite)")
        print("3. Логин пользователя (Сохранить сессию в Redis)")
        print("4. Проверить сессию (Запросить Redis)")
        print("5. Запросить рекламный баннер (Имитация CDN)")
        print("0. Выход")
        
        choice = input("Действие: ")
        
        if choice == "1":
            print_response(requests.get(f"{BASE_URL}/accounts"))
        
        elif choice == "2":
            from_id = int(input("Отправитель (ID счета): "))
            to_id = int(input("Получатель (ID счета): "))
            amount = float(input("Сумма: "))
            print_response(requests.post(f"{BASE_URL}/transfer", json={"from_id": from_id, "to_id": to_id, "amount": amount}))
            
        elif choice == "3":
            client_id = int(input("ID клиента для логина: "))
            res = requests.post(f"{BASE_URL}/login", json={"client_id": client_id})
            print_response(res)
            if res.status_code == 200:
                current_token = res.json().get("token")
                
        elif choice == "4":
            token = input(f"Токен сессии (по умолчанию {current_token}): ") or current_token
            print_response(requests.get(f"{BASE_URL}/session/{token}"))
            
        elif choice == "5":
            filename = input("Имя файла (например banner_credit.jpg): ")
            res = requests.get(f"{BASE_URL}/cdn/ads/{filename}")
            print_response(res)
            print(f"Обратите внимание на заголовок Cache-Control: {res.headers.get('Cache-Control')}")
            
        elif choice == "0":
            break

if __name__ == "__main__":
    run()