def generate_new_board(difficulty):
    #figure out board size/level based on difficulty
    #box_group =  divide board into 3x3 boxes and figure out box groups
    return [[{'value': 0, box_group: None, 'fixed': False} for _ in range(level)] for _ in range(level)]

#loop through game board, if solution board is fixed change value to what it is on solution board

def generate_game_board():
    #add all fixed values from solution board to new board

def generate_solution_board(difficulty):
    #add all the values and the fixed bools to the board

def check_one_solution(board):
