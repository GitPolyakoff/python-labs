import os

def count_directories(paths_list):
    directory_count = 0
    
    for path in paths_list:
        # Проверяем, является ли текущий путь директорией
        if os.path.isdir(path):
            directory_count += 1
            
    return directory_count

# Примеры для проверки работы функции
test_paths = [
    "C:\\Windows",
    "C:\\Windows\\explorer.exe",
    "C:\\Users",
    "some_fake_path_123"
]

print("Количество директорий в списке:", count_directories(test_paths))