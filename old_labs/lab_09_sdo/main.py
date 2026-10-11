import tkinter as tk
import random
from tkinter import messagebox

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Сапер")
        
        self.rows = 10
        self.cols = 10
        self.mines_count = 10
        
        self.buttons = []
        self.mines = []
        self.clicked = []
        
        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        for r in range(self.rows):
            row_buttons = []
            for c in range(self.cols):
                # Создаем кнопку
                btn = tk.Button(self.root, width=3, height=1, font=("Arial", 10, "bold"))
                
                # Привязываем клики мыши (используем lambda, чтобы передать координаты кнопки)
                btn.bind("<Button-1>", lambda event, row=r, col=c: self.on_left_click(row, col))
                btn.bind("<Button-3>", lambda event, row=r, col=c: self.on_right_click(row, col))
                
                # Размещаем кнопку в сетке
                btn.grid(row=r, column=c)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def place_mines(self):
        # Случайная расстановка мин по координатам (строка, колонка)
        count = 0
        while count < self.mines_count:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            
            if (r, c) not in self.mines:
                self.mines.append((r, c))
                count += 1

    def on_left_click(self, r, c):
        # Если клетка уже открыта или на ней стоит флажок, ничего не делаем
        if (r, c) in self.clicked or self.buttons[r][c]["text"] == "F":
            return
        
        self.clicked.append((r, c))
        
        # Проигрыш: попали на мину
        if (r, c) in self.mines:
            self.buttons[r][c].config(text="*", bg="red")
            messagebox.showerror("Поражение", "Вы наткнулись на мину!")
            self.root.destroy()
            return
        
        # Считаем количество мин вокруг нажатой клетки
        mines_around = self.count_mines(r, c)
        
        if mines_around > 0:
            self.buttons[r][c].config(text=str(mines_around), state="disabled", bg="lightgrey")
        else:
            self.buttons[r][c].config(text="", state="disabled", bg="lightgrey")
            # Если вокруг мин нет, автоматически открываем соседние клетки
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= r + i < self.rows and 0 <= c + j < self.cols:
                        self.on_left_click(r + i, c + j)
                        
        # Проверка на победу (открыты все клетки, кроме мин)
        if len(self.clicked) == (self.rows * self.cols) - self.mines_count:
            messagebox.showinfo("Победа", "Вы выиграли!")
            self.root.destroy()

    def on_right_click(self, r, c):
        # Ставим или убираем флажок на закрытой клетке
        if (r, c) not in self.clicked:
            if self.buttons[r][c]["text"] == "F":
                self.buttons[r][c].config(text="", fg="black")
            else:
                self.buttons[r][c].config(text="F", fg="red")

    def count_mines(self, r, c):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (r + i, c + j) in self.mines:
                    count += 1
        return count

# Запуск приложения
if __name__ == "__main__":
    window = tk.Tk()
    game = Minesweeper(window)
    window.mainloop()