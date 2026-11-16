import random as rd

class Minesweeper:
    def __init__(self, level):
        self.level = level
        self.board_rows, self.board_cols, self.bombs = self.assign_by_level()
        self.first_click_rows, self.first_click_cols = []
        self.first_click = False
        self.board = [[{"Bomb": False, "Value": 0, "Revealed": False, "Flagged": False} for _ in range(self.board_cols)] for _ in range(self.board_rows)]
        
        self.game_over = False
        self.won = False


    def click(self, row, col):
        if self.game_over or self.board[row][col]["Flagged"]:
            return

        if self.first_click == False:
            self.first_click_rows, self.first_click_cols = self.no_bomb_area(row, col)
            self.assign_bombs_and_values()
            self.first_click = True

        if self.board[row][col]["Bomb"] == True:
            self.board[row][col]["Revealed"] = True
            self.game_over = True
            return

        self.flood_fill(row, col)

        self.game_over = self.has_won()

    def flood_fill(self, row, col):
        if (not (0 <= row < self.board_rows) or not (0 <= col < self.board_cols)
            or self.board[row][col]["Revealed"]
            or self.board[row][col]["Flagged"]):
            return

        self.board[row][col]["Revealed"] = True

        if self.board[row][col]["Value"] != 0:
            return

        for i in range(-1, 2):
            for j in range(-1, 2):
                self.flood_fill(row + i, col + j)


    def flag(self, row, col):
        if self.board[row][col]["Revealed"] == False and not self.game_over:
            self.board[row][col]["Flagged"] = not self.board[row][col]["Flagged"]


    def has_won(self):
        for row in self.board:
            for tile in row:
                if tile["Bomb"] == False and tile["Revealed"] == False:
                    return False

        self.won = True
        self.game_over = True
        return True
                


    def assign_bombs_and_values(self):
        amount_bombs = 0
        while amount_bombs < self.bombs:
            valid = False
            rd_row = 0
            rd_col = 0
            while not valid:
                rd_row = rd.choice(range(self.board_rows))
                rd_col = rd.choice(range(self.board_cols))

                if (not (rd_row in self.first_click_rows and rd_col in self.first_click_cols)
                    and self.board[rd_row][rd_col]["Bomb"] != True):
                    valid = True

            self.board[rd_row][rd_col]["Bomb"] = True
            amount_bombs += 1
            self.assign_values(rd_row, rd_col)

    def no_bomb_area(self, row, col):
        area_rows = []
        area_cols = []
    
        for i in range(-1, 2):
            if 0 <= row + i < self.board_rows:
                area_rows.append(row + i)
            if 0 <= col + i < self.board_cols:
                area_cols.append(col + i)
    
        return area_rows, area_cols

    def assign_values(self, bomb_row, bomb_col):
        for row in range(-1, 2):
            for col in range(-1, 2):
                new_row = bomb_row + row
                new_col = bomb_col + col
                if (row != 0 or col != 0) and (0 <= new_row < self.board_rows) and (0 <= new_col < self.board_cols):
                    self.board[new_row][new_col]["Value"] += 1
                

    def assign_by_level(self):
        board_rows = (9 if self.level == 1 else 16)
        board_cols = (9 if self.level == 1 else(16 if self.level == 2 else 30))
        bombs = (10 if self.level == 1 else(40 if self.level == 2 else 99))

        return board_rows, board_cols, bombs

