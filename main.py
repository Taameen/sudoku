from __future__ import print_function, division
import random

##################################################################
#                           main.py
#
# Данный файл включает в себя основную реализацию проекта Sudoku, сос-
# тоящую из алгоритма создания нового поля судоку, а также из преобра-
# зования полученной сетки в удобный для печати формат.
##################################################################


def _solve_sudoku(grid_size, board):
    """Solve Sudoku and yield all possible solutions"""
    n = grid_size[0] * grid_size[1]
    
    def is_valid(board, row, col, num):
        if num in board[row]:
            return False
        if num in [board[i][col] for i in range(n)]:
            return False
        box_row = (row // grid_size[0]) * grid_size[0]
        box_col = (col // grid_size[1]) * grid_size[1]
        for i in range(box_row, box_row + grid_size[0]):
            for j in range(box_col, box_col + grid_size[1]):
                if board[i][j] == num:
                    return False
        return True
    
    def solve(board):
        for i in range(n):
            for j in range(n):
                if board[i][j] == 0:
                    for num in range(1, n + 1):
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            for solution in solve(board):
                                yield solution
                            board[i][j] = 0
                    return
        yield [row[:] for row in board]
    
    return solve(board)


class Grid(object):
    """Sudoku grid generator and manipulator"""
    
    def __init__(self, n=3, print_callback=lambda *args, **kwargs: None):
        self.__n = n
        self._print = print_callback
        self.__table = [[((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)] for i in range(n * n)]
        self._print("The base table is ready!")

    # Свойства для безопасного доступа к полям
    @property
    def n(self):
        return self.__n

    @property
    def table(self):
        # Возвращаем копию, чтобы предотвратить внешнюю мутацию внутреннего состояния
        return [row[:] for row in self.__table]

    def show(self):
        """Print the current grid"""
        for row in self.__table:
            self._print(row)

    def transpose(self):
        """Transpose grid"""
        self.__table = [list(x) for x in zip(*self.__table)]

    def swap_rows(self):
        """Swap two rows within a random area"""
        line1, line2 = random.sample(range(self.__n), 2)
        area = random.randrange(self.__n)
        
        n1 = area * self.__n + line1
        n2 = area * self.__n + line2
        
        self.__table[n1], self.__table[n2] = self.__table[n2], self.__table[n1]

    def swap_columns(self):
        """Swap two columns within a random area"""
        self.transpose()
        self.swap_rows()
        self.transpose()

    def swap_rows_area(self):
        """Swap two horizontal areas"""
        area1, area2 = random.sample(range(self.__n), 2)
        
        for i in range(self.__n):
            n1 = area1 * self.__n + i
            n2 = area2 * self.__n + i
            self.__table[n1], self.__table[n2] = self.__table[n2], self.__table[n1]

    def swap_columns_area(self):
        """Swap two vertical areas"""
        self.transpose()
        self.swap_rows_area()
        self.transpose()

    def mix(self, amt=10):
        """Apply random transformations to the grid"""
        mix_func = (
            self.transpose,
            self.swap_rows,
            self.swap_columns,
            self.swap_rows_area,
            self.swap_columns_area,
        )
        for _ in range(amt):
            random.choice(mix_func)()

    def generate_puzzle(self):
        """Generate a Sudoku puzzle with a unique solution"""
        grid_dim = self.__n * self.__n
        total_cells = grid_dim * grid_dim
        
        flook = [[0] * grid_dim for _ in range(grid_dim)]
        iterator = 0
        difficult = total_cells

        while iterator < total_cells:
            i = random.randrange(grid_dim)
            j = random.randrange(grid_dim)
            
            if flook[i][j] == 0:
                iterator += 1
                flook[i][j] = 1
                
                temp = self.__table[i][j]
                self.__table[i][j] = 0
                difficult -= 1
                
                table_solution = [row[:] for row in self.__table]
                
                i_solution = 0
                for _ in _solve_sudoku((self.__n, self.__n), table_solution):
                    i_solution += 1
                    if i_solution > 1:
                        break  # Оптимизация: нет смысла искать все решения, если их уже больше 1
                
                if i_solution != 1:
                    self.__table[i][j] = temp
                    difficult += 1
                    
        return difficult


if __name__ == "__main__":
    example = Grid(n=3, print_callback=print)
    example.mix()
    
    example.show()
    
    example._print("-" * 25)
    
    difficult = example.generate_puzzle()
    
    example.show()
    example._print("difficult =", difficult)

# Вывод в формат ПДФ ещё не доделан, но появится в ближайшее время

