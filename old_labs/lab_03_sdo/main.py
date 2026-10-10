def get_unique_elements(input_list):
    # Преобразуем список во множество (дубликаты удаляются автоматически),
    # а затем через генераторное выражение создаем из него новый список
    return [item for item in set(input_list)]

# Примеры для проверки работы функции
print(get_unique_elements([1, 2, 2, 3, 4, 4, 5]))
print(get_unique_elements(['a', 'b', 'a', 'c', 'b', 'd']))
print(get_unique_elements([10, 10, 10, 10]))