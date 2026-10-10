def create_dict_from_lists(list1, list2):
    result_dict = {}
    
    # Находим минимальную длину, чтобы не выйти за пределы списков 
    # и не учитывать последние элементы большего списка
    min_length = len(list1)
    if len(list2) < min_length:
        min_length = len(list2)
        
    index = 0
    while index < min_length:
        key = list1[index]
        value = list2[index]
        
        # Добавляем пару ключ-значение в словарь
        result_dict.update({key: value})
        
        index += 1
        
    return result_dict

# Примеры для проверки работы функции с разными условиями
print("Одинаковая длина:", create_dict_from_lists(['a', 'b', 'c'], [1, 2, 3]))
print("Второй список больше:", create_dict_from_lists(['a', 'b'], [1, 2, 3, 4]))
print("Первый список больше:", create_dict_from_lists(['a', 'b', 'c', 'd'], [1, 2]))
print("Один список пустой:", create_dict_from_lists([], [1, 2]))
print("Оба списка пустые:", create_dict_from_lists([], []))