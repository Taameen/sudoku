import random

##################################################################
#                           main.py
#
# Данный файл включает в себя основную реализацию проекта Sudoku, сос-
# тоящую из алгоритма создания нового поля судоку, а также из преобра-
# зования полученной сетки в удобный для печати формат.
##################################################################

GRID_SIZE = 3

class Grid:
    def __init__(self, n = GRID_SIZE): # конструктор для создания таблицы n*n
        self.n = n
        self.table = [[((i*n +i/n + j) % (n*n) + 1) for j in range (n*n)] for i in range (n*n)]
        print("The base-table is ready!" )

    def __del__(self):
        pass

    def show(self):
        for i in range (self.n*self.n):
            print self.table[i]

    def transposing(self):
        self.table = map (list, zip(*self.table))

# Метод для перестановки двух строк в пределах одного сектора
    def swap_rows(self):
        area = random.randchange(0, self.n, 1)
        line1 = random.randchange(0, self.n, 1)
        N1 = area*self.n + line1

        line2 = random.randchange(0, self.n, 1)
        while (line1 == line2):
            line2 = random.randchange(0, self.n, 1)

        N2 = area*self.n + line2

        self.table[N1], self.table[N2] = self.table[N2], self.table[N1]

# Метод для перестановки двух столбцов в пределах одного сектора
    def swap_columns(self):
        grid.transposing(self)
        grid.swap_rows(self)
        grid.transoding(self)

# Удаление "лишних" клеток

