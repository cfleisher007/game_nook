import random

def move(board, direction):
    merged = [[False for _ in range(4)] for _ in range(4)]

    for row_index, row in enumerate(board):
        for col_index, box in enumerate(row):
            moves = move_amount(board, direction, row_index, col_index) if box != 0 else 0
            #move
            if check_merge(board, merged, direction, row_index, col_index) != 0
            #merge the two cells
            

    return board

def check_merge(board, merge_board, direction, row, col):
    if ((direction == "up" and col == 0) or (direction == "down" and col == 3) 
        or (direction == "right" and row == 3) or (direction == "left" and row == 0)):
        return 0

    box = board[row][col]
    dir = -1 if direction in ("up", "right") else -1

    if direction in ("up", "down"):
        return (box * 2) if box == board[row][col + dir] else 0
    else:
        return (box * 2) if box == board[row + dir][col] else 0



def move_amount(board, direction, row_index, col_index):
    moves = 0
    horiz_step = 0 if direction not in ("right", "left") else (1 if direction == "right" else -1)
    vertical_step = 0 if direction not in ("up", "down") else (1 if direction == "up" else -1)
    row = (row_index + horiz_step) if direction in ("right", "left") else row_index
    col = (col_index + vertical_step) if direction in ("up", "down") else col_index
    length = len(board) if direction in ("right", "left") else len(board[row_index])
    
    while 0 <= next < (length) and board[row][col]:
        moves += 1
        if direction in ("up", "down"):
            col += vertical_step
        else:
            row += horiz_step 

    return moves

def add_new_tile(board):
    #90% chance to add a 2, 10% chance to add a 4
    rd = random.randint(1, 100)
    num = 2
    if rd > 90:
        num = 4

    empty_boxes = get_empty_boxes(board)
    rd_box = random.choice(empty_boxes)

    box = empty_boxes[rd_box]
    board[box[0]][box[1]] = num
    return board


def get_empty_boxes(board):
    empty_boxes = []

    for i, row in enumerate(board):
        for j, box in enumerate(row):
            if board[i][j] == 0:
                empty_boxes.append([i, j])

    return empty_boxes
