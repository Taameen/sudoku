from __future__ import print_function, division
import random
import os

##################################################################
#                       solve_sudoku
#
# Алгоритм, который находит все возможные способы заполнить пустые  
# клетки судоку, не нарушая правила. Он необходим для проверки на-
# личия единственного решения. Если такого решения нет или оно не
# единственное, удалениие ячейки отменяем.
##################################################################


def solve_sudoku(grid_size, board):
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



##################################################################
#                      generate_algorithm_doc
#
# Создаёт .md-файл с пошаговым текстовым описанием алгоритма созда-
# ния (генерации) судоку, а также с правилами решения судоку.
##################################################################

def generate_algorithm_doc(filename="ALGORITHM.md"):
    description = """# Алгоритм генератора Судоку

## Правила игры
1. Цифра может появиться только один раз в каждой строчке.
2. Цифра может появиться только один раз в каждом столбце.
3. Цифра может появиться только один раз в каждом секторе (квадрат 3x3).

## Основные этапы работы алгоритма:

### 1. Создание базовой сетки 
Генерация начинается с создания математически корректной сетки. 
Используется формула сдвига: `value = ((i * n + i // n + j) % (n * n) + 1)`.
Это гарантирует, что в каждой строке, столбце и блоке все цифры уникальны.

### 2. Перемешивание
К базовой сетке применяются случайные, но валидные преобразования, не нарушающие правила:
- Транспонирование: Отражение сетки относительно главной диагонали.
- Перестановка строк/столбцов в пределах блока: Обмен местами только внутри одного блока 3x3.
- Перестановка целых блоков: Горизонтальные или вертикальные блоки меняются местами целиком.

### 3. Создание головоломки
После получения полностью заполненной сетки начинается удаление цифр:
1. Выбирается случайная ячейка, её значение временно удаляется (заменяется на 0).
2. Запускается алгоритм решения (Backtracking), подсчитывающий количество решений.
3. Если решений больше одного, удаление отменяется (головоломка должна иметь строго одно решение).
4. Если решение одно, цифра считается успешно удаленной.
5. Процесс повторяется до исчерпания лимита попыток.
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(description)
    print(f"[OK] Документация сохранена в: {filename}")



##################################################################
#                           Grid
#
# Ключевой класс Grid. Он отвечает за генерацию заполненного (ре-
# шённого) судоку. Путём валидных преобразований базовая сетка
# перемешивается и на выходе получаем непредсказуемую заполненную
# сетку (без удалённых клеток).
##################################################################

class Grid(object):
    
    def __init__(self, n=3, print_callback=lambda *args, **kwargs: None):
        self.__n = n
        self._print = print_callback
        self.__table = [[((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)] for i in range(n * n)]
        self._print("Базовая таблица готова!")

    @property
    def n(self):
        return self.__n

    @property
    def table(self):
        return [row[:] for row in self.__table]

    def to_string(self, empty_char="."):
        """Возвращает строковое представление сетки """
        n = self.__n
        grid_dim = n * n
        h_separator = "+" + "+".join(["-" * (n * 2 + 1)] * n) + "+\n"
        
        result = h_separator
        for i in range(grid_dim):
            row_str = "|"
            for j in range(grid_dim):
                val = self.__table[i][j]
                cell = f" {empty_char} " if val == 0 else f" {val} "
                row_str += cell
                if (j + 1) % n == 0:
                    row_str += "|"
            
            result += row_str + "\n"
            if (i + 1) % n == 0:
                result += h_separator
        return result

    def show(self):         # Выводит красивую текстовую сетку в консоль
        self._print(self.to_string())

    def transpose(self):    # Транспонирование сетки
        self.__table = [list(x) for x in zip(*self.__table)]

    def swap_rows(self):    # Перестановка двух строк в пределах одного блока
        line1, line2 = random.sample(range(self.__n), 2)
        area = random.randrange(self.__n)
        n1 = area * self.__n + line1
        n2 = area * self.__n + line2
        self.__table[n1], self.__table[n2] = self.__table[n2], self.__table[n1]

    def swap_columns(self): # Перестановка двух столбцов в пределах одного блока
        self.transpose()
        self.swap_rows()
        self.transpose()

    def swap_rows_area(self):   # Перестановка двух горизонтальных блоков
        area1, area2 = random.sample(range(self.__n), 2)
        for i in range(self.__n):
            n1 = area1 * self.__n + i
            n2 = area2 * self.__n + i
            self.__table[n1], self.__table[n2] = self.__table[n2], self.__table[n1]

    def swap_columns_area(self): # Перестановка двух вертикальных блоков
        self.transpose()
        self.swap_rows_area()
        self.transpose()

    def mix(self, amt=10):  # Применение 10 случайных валидных преобразований к сетке.
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
        """Генерация головоломки с единственным решением. Возвращает количество удаленных ячеек"""
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
                
                for _ in solve_sudoku((self.__n, self.__n), table_solution):
                    i_solution += 1
                    if i_solution > 1:
                        break
                
                if i_solution != 1:
                    self.__table[i][j] = temp
                    difficult += 1
                    
        return total_cells - difficult

    def export_to_html(self, filename="sudoku.html", title="Головоломка Судоку"):
        """Экспорт текущего состояния сетки в HTML-файл, готовый к печати через браузер"""
        n = self.__n
        grid_dim = n * n
        
        # Формируем HTML-таблицу
        html_rows = []
        for i in range(grid_dim):
            cells = []
            for j in range(grid_dim):
                val = self.__table[i][j]
                # Пустые ячейки помечаем классом 'empty'
                cell_class = 'empty' if val == 0 else ''
                # Добавляем классы для утолщения границ блоков
                right_border = 'thick-right' if (j + 1) % n == 0 and j != grid_dim - 1 else ''
                bottom_border = 'thick-bottom' if (i + 1) % n == 0 and i != grid_dim - 1 else ''
                
                classes = ' '.join(filter(None, [cell_class, right_border, bottom_border]))
                text = str(val) if val != 0 else ''
                cells.append(f'<td class="{classes}">{text}</td>')
            html_rows.append('<tr>' + ''.join(cells) + '</tr>')
        
        table_html = '\n'.join(html_rows)
        
        html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            color: #222;
        }}
        h1 {{
            text-align: center;
            font-size: 28px;
            margin-bottom: 20px;
            color: #1a1a1a;
        }}
        .rules {{
            background: #f5f5f5;
            padding: 15px 25px;
            border-left: 4px solid #333;
            margin-bottom: 30px;
            font-size: 15px;
            line-height: 1.6;
        }}
        .rules h2 {{
            margin: 0 0 10px 0;
            font-size: 18px;
        }}
        .rules ol {{
            margin: 0;
            padding-left: 20px;
        }}
        table {{
            border-collapse: collapse;
            margin: 0 auto;
            background: white;
        }}
        td {{
            width: 45px;
            height: 45px;
            text-align: center;
            vertical-align: middle;
            font-size: 22px;
            font-weight: bold;
            border: 1px solid #666;
        }}
        td.empty {{
            background: #fafafa;
            color: transparent;
        }}
        td.thick-right {{
            border-right: 3px solid #111;
        }}
        td.thick-bottom {{
            border-bottom: 3px solid #111;
        }}
        /* Утолщаем внешние границы таблицы */
        tr:first-child td {{ border-top: 3px solid #111; }}
        tr:last-child td {{ border-bottom: 3px solid #111; }}
        td:first-child {{ border-left: 3px solid #111; }}
        td:last-child {{ border-right: 3px solid #111; }}
        
        /* Стили для печати */
        @media print {{
            body {{ margin: 0; padding: 10mm; }}
            .no-print {{ display: none; }}
        }}
        .print-hint {{
            text-align: center;
            color: #666;
            font-size: 13px;
            margin-top: 20px;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    
    <div class="rules">
        <h2>Правила решения:</h2>
        <ol>
            <li>Цифра может появиться только один раз в каждой строчке.</li>
            <li>Цифра может появиться только один раз в каждом столбце.</li>
            <li>Цифра может появиться только один раз в каждом секторе (квадрат 3×3).</li>
        </ol>
    </div>
    
    <table>
        {table_html}
    </table>
    
    <p class="print-hint no-print">💡 Нажмите <b>Ctrl+P</b> (или <b>Cmd+P</b> на Mac), чтобы распечатать или сохранить как PDF</p>
</body>
</html>
"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[OK] Судоку успешно сохранено в: {os.path.abspath(filename)}")
        print(f"     Откройте файл в браузере и нажмите Ctrl+P для печати.")


if __name__ == "__main__":
    print("=" * 50)
    print(" ЗАПУСК ГЕНЕРАТОРА СУДОКУ")
    print("=" * 50)
    

    generate_algorithm_doc()    # 1. Создаем файл с описанием алгоритма и правилами
    
    example = Grid(n=3, print_callback=print)    # 2. Инициализируем сетку 3x3 (классическое судоку 9x9)
    
    print("\n[1/4] Перемешивание базовой сетки...")    # 3. Перемешиваем
    example.mix(amt=15)
    
    print("\n[2/4] Полное решение (для проверки):")    # 4. Показываем полное решение
    example.show()
    
    print("\n[3/4] Генерация головоломки (подбор единственного решения)...")    # 5. Генерируем головоломку
    removed_cells = example.generate_puzzle()
    
    print(f"\n[4/4] Итоговая головоломка (удалено ячеек: {removed_cells}):")    # 6. Показываем итоговую головоломку
    example.show()
    
    print("\n[ЭКСПОРТ] Создание файла для печати...")    # 7. Экспорт в HTML
    example.export_to_html("sudoku_printable.html", title="Судоку: Ежедневная головоломка")
    
    print("\n" + "=" * 50)
    print(" РАБОТА ЗАВЕРШЕНА УСПЕШНО")
    print("=" * 50)
