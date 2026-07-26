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
        for i in range (self.n*delf.n):
            print self.table[i]

    
