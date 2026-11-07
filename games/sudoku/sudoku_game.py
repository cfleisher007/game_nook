from game.generator import generate_solution_board, generate_game_board
from game.board import SudokuBoard

solution_board = generate_solution_board(difficulty)
board = SudokuBoard(generate_game_board())