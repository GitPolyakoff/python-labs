import requests
import json

BASE_URL = "http://127.0.0.1:5000/accounts"

def print_response(response):
    print(f"\n--- HTTP CODE: {response.status_code} ---")
    if response.text:
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except:
            print(response.text)
    else:
        print("Пустой ответ (No Content)")

def run_client():
    while True:
        print("\n=========================")
        print("       REST CLIENT       ")
        print("=========================")
        print("1. Получить список")
        print("2. Получить объект")
        print("3. Создать")
        print("4. Изменить полностью (PUT)")
        print("5. Изменить частично (PATCH)")
        print("6. Удалить")
        print("7. Фильтрация (статус=active)")
        print("8. Сортировка (по балансу desc)")
        print("9. Специализированная операция (Total Funds)")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        try:
            if choice == "1":
                res = requests.get(BASE_URL)
                print_response(res)
                
            elif choice == "2":
                acc_id = input("ID счета: ")
                res = requests.get(f"{BASE_URL}/{acc_id}")
                print_response(res)
                
            elif choice == "3":
                name = input("Имя клиента: ")
                bal = float(input("Баланс: "))
                data = {"client_name": name, "currency": "RUB", "balance": bal, "status": "active"}
                res = requests.post(BASE_URL, json=data)
                print_response(res)
                
            elif choice == "4":
                acc_id = input("ID счета: ")
                name = input("Новое имя: ")
                bal = float(input("Новый баланс: "))
                data = {"client_name": name, "currency": "RUB", "balance": bal, "status": "active"}
                res = requests.put(f"{BASE_URL}/{acc_id}", json=data)
                print_response(res)
                
            elif choice == "5":
                acc_id = input("ID счета: ")
                status = input("Новый статус (active/blocked/closed): ")
                res = requests.patch(f"{BASE_URL}/{acc_id}", json={"status": status})
                print_response(res)
                
            elif choice == "6":
                acc_id = input("ID счета для удаления: ")
                res = requests.delete(f"{BASE_URL}/{acc_id}")
                print_response(res)
                
            elif choice == "7":
                res = requests.get(f"{BASE_URL}?status=active")
                print_response(res)
                
            elif choice == "8":
                res = requests.get(f"{BASE_URL}?sort=balance&order=desc")
                print_response(res)
                
            elif choice == "9":
                res = requests.get(f"{BASE_URL}/total-funds")
                print_response(res)
                
            elif choice == "0":
                break
            else:
                print("Неверный выбор")
                
        except requests.exceptions.ConnectionError:
            print("\nОШИБКА: Сервер недоступен. Убедитесь, что app.py запущен.")

if __name__ == "__main__":
    run_client()