def print_list_with_semicolon(my_list):
    # Распаковываем список с помощью * и указываем точку с запятой как разделитель
    print(*my_list, sep=';')

# Примеры для проверки работы функции
print_list_with_semicolon([1, 2, 3, 4, 5])
print_list_with_semicolon(['яблоко', 'банан', 'груша'])
print_list_with_semicolon([10.5, 'текст', 42])