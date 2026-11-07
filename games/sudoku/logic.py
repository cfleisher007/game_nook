#return a list of valid numbers for a cell on a board
def get_valid_numbers(board, row, col):
    valid_nums = list(range(1, 10))

    for row_index, row_cell in enumerate(board):
        col_cell = row_cell[col]
        if col_cell["value"] in valid_nums:
            valid_nums.remove(col_cell["value"])

    for row_cell in board[row]:
        if row_cell["value"] in valid_nums:
            valid_nums.remove(row_cell["value"])

    starting_row = (row // 3) * 3
    starting_col = (col // 3) * 3
    for box_row in range(starting_row, starting_row + 3):
        for box_col in range(starting_col, starting_col + 3):
            box_cell = board[box_row][box_col]
            if box_cell["value"] in valid_nums:
                valid_nums.remove(box_cell["value"])


def is_valid_sudoku(board):
    #check rows
    for row in board:
        if not check_row(row):
            return False

    #check columns
    for col in range(len(board)):
        if not check_column([board[row][col] for col in range(len(board))]):
            return False

    #check boxes
    for box_row in range(0, len(board), 3):
        for box_col in range(0, len(board), 3):
            box = [board[row][col] for row in range(box_row, box_row + 3) for col in range(box_col, box_col + 3)]
            if not check_box(box):
                return False

    return True

def check_row(row):
    new_row = [num for num in row if num != 0]
    seen = set(new_row)
    if len(new_row) == len(seen):
        return True
    else:
        return False

def check_column(col):
    new_col = [num for num in col if num != 0]
    seen = set(new_col)
    if len(new_col) == len(seen):
        return True
    else:
        return False

def check_box(box):
    new_box = [num for num in box if num != 0]
    seen = set(new_box)
    if len(new_box) == len(seen):
        return True
    else:
        return False