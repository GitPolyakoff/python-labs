import os
from PIL import Image

def swap_pixels(image_path, list_coords1, list_coords2):
    # Открываем изображение
    img = Image.open(image_path)
    
    # Получаем доступ к карте пикселей
    pixels = img.load()
    
    # Проверяем, что списки одинаковой длины, чтобы каждому пикселю нашлась пара
    if len(list_coords1) != len(list_coords2):
        print("Ошибка: Списки координат должны быть одинаковой длины!")
        return
    
    # Перебираем координаты и меняем пиксели местами
    for i in range(len(list_coords1)):
        coord1 = list_coords1[i]
        coord2 = list_coords2[i]
        
        # Получаем цвета пикселей
        color1 = pixels[coord1[0], coord1[1]]
        color2 = pixels[coord2[0], coord2[1]]
        
        # Перемещаем пиксели
        pixels[coord1[0], coord1[1]] = color2
        pixels[coord2[0], coord2[1]] = color1
        
    current_dir = os.path.dirname(image_path)
    new_path = os.path.join(current_dir, "swapped_image.jpg")
    
    img.save(new_path)
    print(f"Изображение успешно сохранено по пути: {new_path}")

script_dir = os.path.dirname(os.path.abspath(__file__))
target_image = os.path.join(script_dir, "image.jpg")

# Создаем два списка координат (x, y)
coords_list_1 = [(0, 0), (1, 1), (2, 2), (3, 3)]
coords_list_2 = [(10, 10), (11, 11), (12, 12), (13, 13)]

swap_pixels(target_image, coords_list_1, coords_list_2)