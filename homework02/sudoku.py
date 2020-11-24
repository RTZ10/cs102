import time
from random import randint
from typing import List, Optional, Set, Tuple

from pkg_resources._vendor.appdirs import system


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    cou = len(values) - 1
    return [[values[pos] for pos in range(i, i + n)] for i in range(0, cou, n)]


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row = pos[0]
    import math

    blocks_in_row = int(math.sqrt(len(grid) * len(grid[0])) / len(grid[0]))
    mas = []
    for i in range(blocks_in_row * row, blocks_in_row * (row + 1)):
        for j in range(len(grid[0])):
            mas.append(grid[i][j])
    return mas


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    num_of_el = pos[1]
    import math

    pos_in_row = int(math.sqrt(len(grid) * len(grid[0])))
    mas = []
    while num_of_el < pos_in_row * pos_in_row:
        mas.append(grid[int(num_of_el / len(grid[0]))][num_of_el % len(grid[0])])
        num_of_el += pos_in_row
    return mas


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    mas = []
    import math

    count_of_blocks = len(grid)
    size_of_block = len(grid[0])
    pos_in_row = int(math.sqrt(count_of_blocks * size_of_block))
    row, col = pos
    # найдем позицию левого верхнего элемента искомого блока
    if row % 3 == 1:
        row -= 1
    elif row % 3 == 2:
        row -= 2
    if col % 3 == 1:
        col -= 1
    elif col % 3 == 2:
        col -= 2
    num_of_el = row * pos_in_row + col
    for i in range(3):
        num_of_block_in_grid = int(num_of_el / size_of_block)
        for j in range(3):
            mas.append(grid[num_of_block_in_grid][num_of_el % size_of_block + j])
        num_of_el += pos_in_row
    return mas


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    count_of_blocks = len(grid)
    size_of_block = len(grid[0])
    pos = 0
    for block in range(0, count_of_blocks):
        for pos_in_block in range(0, size_of_block):
            if grid[block][pos_in_block] == ".":
                pos = (block, pos_in_block)
                return pos
    return None


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    pos_val = {i for i in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}}
    for delta in get_row(grid, pos):
        pos_val.discard(delta)
    for delta1 in get_col(grid, pos):
        pos_val.discard(delta1)
    for delta2 in get_block(grid, pos):
        pos_val.discard(delta2)

    return pos_val


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if pos is not None:
        block, pos_in_block = pos
        var = find_possible_values(grid, pos)
        if len(var) == 0:
            return None
        for i in var:
            grid[block][pos_in_block] = i
            if solve(grid) is None:
                grid[block][pos_in_block] = "."
            else:
                return grid
    else:
        return grid


def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    necessary_numbers = [num for num in range(1, 10)]
    for i in range(len(solution)):
        for j in range(len(solution[0])):
            numbers_in_block = get_block(solution, (i, j))
            numbers_in_row = get_row(solution, (i, j))
            numbers_in_col = get_col(solution, (i, j))
            for num in necessary_numbers:
                if numbers_in_col.count(str(num)) != 1 or numbers_in_row.count(str(num)) != 1:
                    return False
                if numbers_in_block.count(str(num)) != 1:
                    return False
    return True


def generate_sudoku(N: int) -> List[List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    sudoku = [["." for i in range(0, 9)] for j in range(0, 9)]
    sudoku = solve(sudoku)
    N = max(81 - N, 0)
    while N > 0:
        row = randint(0, 8)
        col = randint(0, 8)
        while sudoku[row][col] == ".":
            row = randint(0, 8)
            col = randint(0, 8)
        sudoku[row][col] = "."
        N -= 1
    return sudoku


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
