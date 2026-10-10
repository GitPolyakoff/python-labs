def calculate_average(values):
    return sum(values) / len(values)

def get_above_average_count(values, average_value):
    count = 0
    for value in values:
        if value > average_value:
            count += 1
    return count

def main():
    count = int(input("Введите количество сеансов: "))

    if count <= 0:
        print("Ошибка: количество сеансов должно быть больше нуля.")
        return

    tickets_sold = []
    revenues = []

    for i in range(count):
        print(f"Сеанс {i + 1}")
        
        tickets = int(input("Введите количество проданных билетов: "))
        if tickets < 0: tickets = 0
            
        price = float(input("Введите стоимость одного билета: "))
        if price < 0: price = 0.0

        session_revenue = tickets * price
        print(f"Выручка сеанса: {session_revenue:.2f}")

        tickets_sold.append(tickets)
        revenues.append(session_revenue)

    total_revenue = sum(revenues)
    max_revenue = max(revenues)
    best_session_number = revenues.index(max_revenue) + 1
    average_tickets = calculate_average(tickets_sold)
    above_average_count = get_above_average_count(tickets_sold, average_tickets)

    print(f"Общая выручка всех сеансов: {total_revenue:.2f}")
    print(f"Самый прибыльный сеанс: {best_session_number} (выручка {max_revenue:.2f})")
    print(f"Среднее количество проданных билетов: {average_tickets:.2f}")
    print(f"Количество сеансов с продажами выше среднего: {above_average_count}")

if __name__ == "__main__":
    main()