from game.logic import get_valid_numbers

#find an empty cell
#try a valid number
#recursively continue
#if solved, increment a solution counter
#backtrack and keep searching
#stop once found 2 solutions

def solutions(board):
    counter = [0]
    return count_solutions(board, counter)

def count_solutions(board, solution_counter):
    if solution_counter == 2:
        return False

    #if no solutions left and solution_counter < 2, return True
    
    for row in enumerate(board):
        for col in range(len(board)):
            if board[row][col]["value"] == 0:
                valid_nums = get_valid_numbers(board, row, col)
                