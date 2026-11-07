import random as rd

def move(board, direction):
    new_board = []
    if direction in ("up", "down"):
        for c in range(4):
            column_list = [board[r][c] for r in range(4)]
            processed_list = slide_and_merge_line(column_list)
            for r in range(4):
                board[r][c] = processed_list[r]
    else:
        for row_index, row in enumerate(board):
            board[row_index] = slide_and_merge_line(row)

    add_new_tile(board)

def slide_and_merge_line(line):
    non_zeros = [num for num in line if num != 0]

    merged = []
    skip = False
    for i in range(len(non_zeros)):
        if skip:
            skip = False
            continue
        if i + 1 < len(non_zeros) and non_zeros[i] == non_zeros[i + 1]:
            merged.append(non_zeros[i] * 2)
            skip = True
        else:
            merged.append(non_zeros[i])

    while len(merged) < 4:
        merged.append(0)

    return merged


def add_new_tile(board):
    #90% chance to add a 2, 10% chance to add a 4
    rdm = rd.randint(1, 100)
    num = 2
    if rdm > 90:
        num = 4

    empty_boxes = get_empty_boxes(board)
    rd_box = rd.choice(empty_boxes)
    board[rd_box[0]][rd_box[1]] = num


def get_empty_boxes(board):
    empty_boxes = []

    for i, row in enumerate(board):
        for j, box in enumerate(row):
            if board[i][j] == 0:
                empty_boxes.append([i, j])

    return empty_boxes

def print_board(board):
    string = ""
    for row in board:
        for box in row:
            string += str(box)

        string += " "
    
    print(string)
    