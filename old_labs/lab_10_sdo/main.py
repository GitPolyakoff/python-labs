import numpy as np
import matplotlib.pyplot as pt

def create_random_scatter():
    # Генерируем 50 случайных точек по X и Y
    x = np.random.randint(0, 100, size=50)
    y = np.random.randint(0, 100, size=50)
    
    # Генерируем случайный размер каждого шарика
    sizes = np.random.randint(20, 500, size=50)
    
    # Создаем объект фигуры холст
    figure = pt.figure()
    
    # Строим точечную диаграмму, передавая x, y и размеры шариков
    pt.scatter(x, y, s=sizes)
    
    pt.grid(True)
    
    pt.title("Случайная точечная диаграмма")
    
    pt.show()

create_random_scatter()