#################################################################
# FILE : puzzle_solver.py
# WRITER : Geva Haviv
# DESCRIPTION:
# WEB PAGES I USED:
# NOTES:
#################################################################
import copy
from typing import List, Tuple, Set, Optional


# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """
    This function return the max cells you can 'see' from the cell[row][col] in picture.
    :param picture: Board game with values.
    :param row: Row index.
    :param col: Column index.
    :return: Int.
    """
    if picture[row][col] == 0:
        return 0

    s = 0

    for idx in range(col, len(picture[0]), 1):  # Go right.
        if picture[row][idx] == 0:
            break
        if idx == col:
            continue
        s += 1

    for idx in range(col, -1, -1):              # Go left.
        if picture[row][idx] == 0:
            break
        if idx == col:
            continue
        s += 1

    for idx in range(row, len(picture), 1):     # Go up.
        if picture[idx][col] == 0:
            break
        if idx == row:
            continue
        s += 1

    for idx in range(row, -1, -1):              # Go down.
        if picture[idx][col] == 0:
            break
        if idx == row:
            continue
        s += 1

    s += 1
    return s


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """
    This function return the min cells you can 'see' from the cell[row][col] in picture.
    :param picture: Board game with values.
    :param row: Row index.
    :param col: Column index.
    :return: Int.
    """

    if picture[row][col] == 0 or picture[row][col] == -1:
        return 0

    s = 0

    for idx in range(col, len(picture[0]), 1):  # Go right.
        if picture[row][idx] == 0 or picture[row][idx] == -1:
            break
        if idx == col:
            continue
        s += 1

    for idx in range(col, -1, -1):              # Go left.
        if picture[row][idx] == 0 or picture[row][idx] == -1:
            break
        if idx == col:
            continue
        s += 1

    for idx in range(row, len(picture), 1):     # Go up.
        if picture[idx][col] == 0 or picture[idx][col] == -1:
            break
        if idx == row:
            continue
        s += 1

    for idx in range(row, -1, -1):              # Go down.
        if picture[idx][col] == 0 or picture[idx][col] == -1:
            break
        if idx == row:
            continue
        s += 1

    s += 1
    return s


def _lst_of_constraints_set(picture: Picture, constraints_set: Set[Constraint]) -> list:
    """
    This function calculate the constraints_set according to the picture.
    :param picture: Board game with values.
    :param constraints_set: The index's and values we want to calculate.
    :return: List.
    """

    results_lst = []
    for constraints in constraints_set:
        if min_seen_cells(picture, constraints[0], constraints[1]) == constraints[2] and\
                max_seen_cells(picture, constraints[0], constraints[1]) == constraints[2]:
            results_lst.append(1)
        elif min_seen_cells(picture, constraints[0], constraints[1]) <= constraints[2] <=\
                max_seen_cells(picture, constraints[0], constraints[1]):
            results_lst.append(2)
        else:
            results_lst.append(0)

    return results_lst


def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    """
    This function check the constraints_set according to the picture.
    :param picture: Board game with values.
    :param constraints_set: The index's and values we want to check.
    :return: Int.
    """

    results_lst = _lst_of_constraints_set(copy.deepcopy(picture), constraints_set)
    if 0 in results_lst:
        return 0
    elif 2 in results_lst:
        return 2
    return 1


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    """
    This function return a possible solution for the puzzle.
    :param constraints_set: The index's and values of the board.
    :param n: Number of rows.
    :param m: Number of columns.
    :return: Optional[Picture] (None or solution).
    """

    board = _create_board(n, m)
    return _solve_puzzle_helper(board, constraints_set, n, m)


def _solve_puzzle_helper(board: List[List[int]], constraints_set: Set[Constraint], n: int, m: int) -> any:
    """
    This function is helper and it return a possible solution for the puzzle.
    :param board: Default board set by -1.
    :param constraints_set: The index's and values of the board.
    :param n: Number of rows.
    :param m: Number of columns.
    :return: Any (None or solution).
    """

    for i in range(n):
        for j in range(m):
            if board[i][j] != -1:
                continue

            board[i][j] = 0
            if check_constraints(board, constraints_set) == 2:
                _solve_puzzle_helper(board, constraints_set, n, m)
            if check_constraints(board, constraints_set) == 1:
                return board

            board[i][j] = 1
            if check_constraints(board, constraints_set) == 2:
                _solve_puzzle_helper(board, constraints_set, n, m)
            if check_constraints(board, constraints_set) == 1:
                return board

            board[i][j] = -1
            return


def _create_board(n: int, m: int) -> List[List[int]]:
    """
    This function create new board and set the board by -1.
    :param n: Number of rows.
    :param m: Number of columns.
    :return: List[List[Int]].
    """

    board = []

    for row in range(n):
        board.append([])
        for column in range(m):
            board[row].append(-1)

    return board


def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    """
    This function return how many solutions the board has.
    :param constraints_set: The index's and values of the board.
    :param n: Number of rows.
    :param m: Number of columns.
    :return: Int.
    """
    board = _create_board(n, m)
    return _how_many_solutions_helper(board, constraints_set, n, m, [])


def _how_many_solutions_helper(board: List[List[int]], constraints_set: Set[Constraint],
                               n: int, m: int, count: list) -> int:
    """
    This function is helper and return how many solutions the board has.
    :param board: Default board set by -1.
    :param constraints_set: The index's and values of the board.
    :param n: Number of rows.
    :param m: Number of columns.
    :return: Int.
    """

    for row in range(n):
        for column in range(m):
            if board[row][column] == -1:
                for new_value in range(2):
                    if check_constraints(board, constraints_set) != 0:
                        board[row][column] = new_value
                        _how_many_solutions_helper(board, constraints_set, n, m, count)
                        board[row][column] = -1

                return len(count)

    if check_constraints(board, constraints_set) == 1:
        count.append(1)


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    ...
